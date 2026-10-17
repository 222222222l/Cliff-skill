#!/usr/bin/env python3
"""Demo trainer for a single-timeframe long-context market Transformer.

This script is intentionally compact and extensible. It demonstrates:

- CSV panel input with symbol/market/time columns.
- Daily sliding-window samples.
- Patch-based Transformer encoder for cost-controlled long context.
- Feature-group gating for dynamic indicator weighting.
- Multi-head outputs: return quantiles, expected return, up probability, position.
- Decision-aware loss with transaction-cost and turnover penalties.

Expected minimum columns:
timestamp,symbol,market,open,high,low,close,volume

Optional feature columns may include technical indicators, signal flags, prior
weights, market context, and event flags. Numeric columns not listed in
--exclude-columns are used as model features.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

try:
    import torch
    from torch import nn
    from torch.nn import functional as F
    from torch.utils.data import DataLoader, Dataset
except ImportError as exc:  # pragma: no cover - useful runtime message.
    raise SystemExit("This demo requires PyTorch. Install torch before training.") from exc


DEFAULT_EXCLUDE_COLUMNS = {
    "timestamp",
    "symbol",
    "market",
}


@dataclass
class PanelRow:
    timestamp: str
    symbol: str
    market: str
    values: Dict[str, float]


def parse_float(value: str) -> float:
    if value is None or str(value).strip() == "":
        return float("nan")
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return float("nan")


def load_panel_csv(path: str, exclude_columns: Iterable[str]) -> Tuple[List[PanelRow], List[str]]:
    exclude = {col.lower() for col in exclude_columns}
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        fieldnames = [name.strip() for name in reader.fieldnames]
        lower_to_name = {name.lower(): name for name in fieldnames}
        for required in ("timestamp", "symbol", "market", "close"):
            if required not in lower_to_name:
                raise ValueError(f"Missing required column: {required}")

        feature_columns = [
            name for name in fieldnames
            if name.lower() not in exclude and name.lower() not in {"future_return"}
        ]
        rows: List[PanelRow] = []
        for raw in reader:
            values = {col: parse_float(raw.get(col, "")) for col in feature_columns}
            if math.isnan(values.get(lower_to_name["close"], float("nan"))):
                continue
            rows.append(PanelRow(
                timestamp=str(raw[lower_to_name["timestamp"]]),
                symbol=str(raw[lower_to_name["symbol"]]),
                market=str(raw[lower_to_name["market"]]),
                values=values,
            ))
    return rows, feature_columns


class RollingStandardizer:
    """Train-window standardizer with missing-value mask support."""

    def __init__(self) -> None:
        self.mean: torch.Tensor | None = None
        self.std: torch.Tensor | None = None

    def fit(self, arrays: Sequence[torch.Tensor]) -> None:
        stacked = torch.cat(arrays, dim=0)
        mask = torch.isfinite(stacked)
        safe = torch.where(mask, stacked, torch.zeros_like(stacked))
        count = mask.sum(dim=0).clamp_min(1)
        mean = safe.sum(dim=0) / count
        var = torch.where(mask, (stacked - mean) ** 2, torch.zeros_like(stacked)).sum(dim=0) / count
        self.mean = mean
        self.std = torch.sqrt(var).clamp_min(1e-6)

    def transform(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.mean is None or self.std is None:
            raise RuntimeError("Standardizer must be fit before transform.")
        missing_mask = ~torch.isfinite(x)
        x = torch.where(missing_mask, self.mean, x)
        return (x - self.mean) / self.std, missing_mask.float()


class MarketWindowDataset(Dataset):
    """Create per-symbol sliding windows and next-return labels."""

    def __init__(
        self,
        rows: Sequence[PanelRow],
        feature_columns: Sequence[str],
        lookback: int,
        horizon: int,
        symbol_to_id: Dict[str, int],
        market_to_id: Dict[str, int],
        standardizer: RollingStandardizer | None = None,
        fit_standardizer: bool = False,
    ) -> None:
        self.feature_columns = list(feature_columns)
        self.lookback = lookback
        self.horizon = horizon
        self.symbol_to_id = symbol_to_id
        self.market_to_id = market_to_id
        grouped: Dict[str, List[PanelRow]] = defaultdict(list)
        for row in rows:
            grouped[row.symbol].append(row)
        for symbol in grouped:
            grouped[symbol].sort(key=lambda item: item.timestamp)

        self.samples: List[Tuple[torch.Tensor, float, str, str, str, float]] = []
        raw_windows: List[torch.Tensor] = []
        close_lookup = {col.lower(): index for index, col in enumerate(self.feature_columns)}
        close_idx = close_lookup["close"]

        for symbol, symbol_rows in grouped.items():
            matrix = torch.tensor([
                [row.values.get(col, float("nan")) for col in self.feature_columns]
                for row in symbol_rows
            ], dtype=torch.float32)
            closes = matrix[:, close_idx]
            for end in range(lookback - 1, len(symbol_rows) - horizon):
                start = end - lookback + 1
                future_return = torch.log(closes[end + horizon] / closes[end]).item()
                if not math.isfinite(future_return):
                    continue
                window = matrix[start:end + 1]
                raw_windows.append(window)
                self.samples.append((
                    window,
                    future_return,
                    symbol,
                    symbol_rows[end].market,
                    symbol_rows[end].timestamp,
                    closes[end].item(),
                ))

        self.standardizer = standardizer or RollingStandardizer()
        if fit_standardizer:
            self.standardizer.fit(raw_windows)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> Dict[str, object]:
        window, future_return, symbol, market, timestamp, close = self.samples[index]
        x, missing = self.standardizer.transform(window)
        return {
            "x": x,
            "missing_mask": missing,
            "future_return": torch.tensor(future_return, dtype=torch.float32),
            "symbol_id": torch.tensor(self.symbol_to_id[symbol], dtype=torch.long),
            "market_id": torch.tensor(self.market_to_id[market], dtype=torch.long),
            "symbol": symbol,
            "market": market,
            "timestamp": timestamp,
            "close": torch.tensor(close, dtype=torch.float32),
        }


class FeatureGate(nn.Module):
    """Dynamic feature weighting inspired by variable-selection networks."""

    def __init__(self, feature_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.scorer = nn.Sequential(
            nn.LayerNorm(feature_dim * 2),
            nn.Linear(feature_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, feature_dim),
        )

    def forward(self, x: torch.Tensor, missing_mask: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        gate_logits = self.scorer(torch.cat([x, missing_mask], dim=-1))
        gate_logits = gate_logits.masked_fill(missing_mask.bool(), -1e4)
        weights = torch.softmax(gate_logits, dim=-1)
        return x * weights, weights


class PatchEmbedding(nn.Module):
    def __init__(self, feature_dim: int, d_model: int, patch_size: int) -> None:
        super().__init__()
        self.patch_size = patch_size
        self.proj = nn.Linear(feature_dim * patch_size, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, features = x.shape
        usable = length - (length % self.patch_size)
        x = x[:, length - usable:, :]
        x = x.reshape(batch, usable // self.patch_size, features * self.patch_size)
        return self.proj(x)


class MarketTransformer(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        num_symbols: int,
        num_markets: int,
        d_model: int = 128,
        layers: int = 4,
        heads: int = 4,
        patch_size: int = 5,
        dropout: float = 0.15,
    ) -> None:
        super().__init__()
        self.feature_gate = FeatureGate(feature_dim, hidden_dim=max(64, feature_dim * 2))
        self.patch = PatchEmbedding(feature_dim, d_model, patch_size)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
        self.pos_embedding = nn.Parameter(torch.zeros(1, 512, d_model))
        self.symbol_embedding = nn.Embedding(num_symbols, d_model)
        self.market_embedding = nn.Embedding(num_markets, d_model)
        self.adapter_norm = nn.LayerNorm(d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=heads,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=layers)
        self.norm = nn.LayerNorm(d_model)
        self.expected_return = nn.Linear(d_model, 1)
        self.quantiles = nn.Linear(d_model, 3)
        self.up_logit = nn.Linear(d_model, 1)
        self.risk = nn.Sequential(nn.Linear(d_model, 1), nn.Softplus())
        self.position_head = nn.Sequential(nn.Linear(d_model, 1), nn.Tanh())

    def forward(
        self,
        x: torch.Tensor,
        missing_mask: torch.Tensor,
        symbol_id: torch.Tensor,
        market_id: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        gated, feature_weights = self.feature_gate(x, missing_mask)
        tokens = self.patch(gated)
        batch = tokens.shape[0]
        adapter = self.symbol_embedding(symbol_id) + self.market_embedding(market_id)
        adapter = self.adapter_norm(adapter).unsqueeze(1)
        cls = self.cls_token.expand(batch, -1, -1) + adapter
        tokens = torch.cat([cls, tokens], dim=1)
        tokens = tokens + self.position_encoding(tokens.shape[1])
        encoded = self.encoder(tokens)
        pooled = self.norm(encoded[:, 0])
        quantiles = self.quantiles(pooled)
        quantiles = torch.sort(quantiles, dim=-1).values
        return {
            "expected_return": self.expected_return(pooled).squeeze(-1),
            "return_quantiles": quantiles,
            "up_logit": self.up_logit(pooled).squeeze(-1),
            "downside_risk": self.risk(pooled).squeeze(-1),
            "position_score": self.position_head(pooled).squeeze(-1),
            "feature_weights": feature_weights.mean(dim=1),
        }

    def position_encoding(self, length: int) -> torch.Tensor:
        if length <= self.pos_embedding.shape[1]:
            return self.pos_embedding[:, :length, :]
        extra = self.pos_embedding[:, -1:, :].expand(1, length - self.pos_embedding.shape[1], -1)
        return torch.cat([self.pos_embedding, extra], dim=1)


def quantile_loss(pred: torch.Tensor, target: torch.Tensor, quantiles: Sequence[float]) -> torch.Tensor:
    losses = []
    for index, q in enumerate(quantiles):
        error = target - pred[:, index]
        losses.append(torch.maximum((q - 1) * error, q * error).unsqueeze(-1))
    return torch.cat(losses, dim=-1).mean()


def decision_utility_loss(
    position: torch.Tensor,
    future_return: torch.Tensor,
    previous_position: torch.Tensor | None,
    cost_bps: float,
) -> Tuple[torch.Tensor, torch.Tensor]:
    if previous_position is None:
        previous_position = torch.zeros_like(position)
    turnover = torch.abs(position - previous_position)
    cost = cost_bps / 10000.0 * turnover
    net_pnl = position * future_return - cost
    downside = F.relu(-net_pnl).pow(2).mean()
    loss = -net_pnl.mean() + 0.5 * downside + 0.05 * turnover.mean()
    return loss, net_pnl.detach()


def train_epoch(
    model: MarketTransformer,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    cost_bps: float,
) -> Dict[str, float]:
    model.train()
    totals = defaultdict(float)
    count = 0
    previous_position = None
    for batch in loader:
        x = batch["x"].to(device)
        missing = batch["missing_mask"].to(device)
        symbol_id = batch["symbol_id"].to(device)
        market_id = batch["market_id"].to(device)
        target = batch["future_return"].to(device)
        out = model(x, missing, symbol_id, market_id)
        q_loss = quantile_loss(out["return_quantiles"], target, [0.1, 0.5, 0.9])
        direction = (target > 0).float()
        direction_loss = F.binary_cross_entropy_with_logits(out["up_logit"], direction)
        huber = F.huber_loss(out["expected_return"], target)
        utility, pnl = decision_utility_loss(out["position_score"], target, previous_position, cost_bps)
        previous_position = out["position_score"].detach()
        loss = q_loss + 0.5 * direction_loss + 0.25 * huber + 0.5 * utility

        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        batch_size = x.shape[0]
        count += batch_size
        totals["loss"] += loss.item() * batch_size
        totals["quantile_loss"] += q_loss.item() * batch_size
        totals["direction_loss"] += direction_loss.item() * batch_size
        totals["utility_loss"] += utility.item() * batch_size
        totals["mean_net_pnl"] += pnl.mean().item() * batch_size
    return {key: value / max(1, count) for key, value in totals.items()}


@torch.no_grad()
def evaluate(model: MarketTransformer, loader: DataLoader, device: torch.device) -> Dict[str, float]:
    model.eval()
    totals = defaultdict(float)
    count = 0
    for batch in loader:
        x = batch["x"].to(device)
        missing = batch["missing_mask"].to(device)
        symbol_id = batch["symbol_id"].to(device)
        market_id = batch["market_id"].to(device)
        target = batch["future_return"].to(device)
        out = model(x, missing, symbol_id, market_id)
        up_prob = torch.sigmoid(out["up_logit"])
        pred_direction = up_prob > 0.5
        true_direction = target > 0
        batch_size = x.shape[0]
        count += batch_size
        totals["direction_accuracy"] += (pred_direction == true_direction).float().mean().item() * batch_size
        totals["mean_abs_error"] += torch.abs(out["expected_return"] - target).mean().item() * batch_size
        totals["mean_position"] += out["position_score"].mean().item() * batch_size
    return {key: value / max(1, count) for key, value in totals.items()}


def time_split(rows: Sequence[PanelRow], train_ratio: float) -> Tuple[List[PanelRow], List[PanelRow]]:
    timestamps = sorted({row.timestamp for row in rows})
    cutoff = timestamps[int(len(timestamps) * train_ratio)]
    train = [row for row in rows if row.timestamp <= cutoff]
    valid = [row for row in rows if row.timestamp > cutoff]
    return train, valid


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a demo long-context market Transformer.")
    parser.add_argument("--input", required=True, help="Panel CSV path.")
    parser.add_argument("--lookback", type=int, default=256)
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--patch-size", type=int, default=5)
    parser.add_argument("--d-model", type=int, default=128)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.15)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--cost-bps", type=float, default=5.0)
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--exclude-columns", default=",".join(sorted(DEFAULT_EXCLUDE_COLUMNS)))
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    exclude = [item.strip() for item in args.exclude_columns.split(",") if item.strip()]
    rows, feature_columns = load_panel_csv(args.input, exclude)
    symbol_to_id = {symbol: index for index, symbol in enumerate(sorted({row.symbol for row in rows}))}
    market_to_id = {market: index for index, market in enumerate(sorted({row.market for row in rows}))}
    train_rows, valid_rows = time_split(rows, args.train_ratio)
    train_dataset = MarketWindowDataset(
        train_rows,
        feature_columns,
        lookback=args.lookback,
        horizon=args.horizon,
        symbol_to_id=symbol_to_id,
        market_to_id=market_to_id,
        fit_standardizer=True,
    )
    valid_dataset = MarketWindowDataset(
        valid_rows,
        feature_columns,
        lookback=args.lookback,
        horizon=args.horizon,
        symbol_to_id=symbol_to_id,
        market_to_id=market_to_id,
        standardizer=train_dataset.standardizer,
    )
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True)
    valid_loader = DataLoader(valid_dataset, batch_size=args.batch_size, shuffle=False)

    model = MarketTransformer(
        feature_dim=len(feature_columns),
        num_symbols=len(symbol_to_id),
        num_markets=len(market_to_id),
        d_model=args.d_model,
        layers=args.layers,
        heads=args.heads,
        patch_size=args.patch_size,
        dropout=args.dropout,
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)

    print({
        "device": str(device),
        "features": len(feature_columns),
        "feature_columns": feature_columns,
        "symbols": len(symbol_to_id),
        "markets": len(market_to_id),
        "train_samples": len(train_dataset),
        "valid_samples": len(valid_dataset),
        "outputs": [
            "expected_return",
            "return_quantiles[p10,p50,p90]",
            "up_probability",
            "downside_risk",
            "position_score",
            "feature_weights",
        ],
    })

    for epoch in range(1, args.epochs + 1):
        train_metrics = train_epoch(model, train_loader, optimizer, device, args.cost_bps)
        valid_metrics = evaluate(model, valid_loader, device) if len(valid_dataset) else {}
        print({"epoch": epoch, "train": train_metrics, "valid": valid_metrics})


if __name__ == "__main__":
    main()
