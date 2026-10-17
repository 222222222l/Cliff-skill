# Macro Stress Derivative Analysis

Use this reference when macro analysis needs early crisis detection, transmission-chain mapping, or explicit separation of level, first-derivative, and second-derivative signals across liquidity, rates, credit, labor, inflation, fiscal issuance, and market transmission.

Core idea: do not wait for absolute levels to become extreme. A crisis often starts with a small but persistent first derivative, then becomes dangerous when the second derivative turns positive across multiple linked markets.

## Signal Layers

For each indicator, classify evidence into three layers:

| Layer | Question | Typical Use |
| --- | --- | --- |
| Level / stock | Where is the indicator versus history and policy thresholds? | Current severity and distance from crisis regimes. |
| First derivative | Is it worsening or improving over the latest observation windows? | Early warning and change in marginal pressure. |
| Second derivative | Is the worsening itself accelerating, broadening, or propagating to adjacent markets? | Crisis-chain confirmation and de-risking trigger. |

Use both raw changes and standardized changes:

```text
level_z = (current - rolling_mean) / rolling_std
first_derivative = current - previous_observation
first_derivative_z = first_derivative / rolling_std_of_changes
second_derivative = first_derivative - previous_first_derivative
```

For weekly macro/liquidity data, compare 1-week, 4-week, and 13-week changes. For daily market data, compare 1-day, 5-day, and 20-day changes. For monthly labor/inflation data, compare 1-month, 3-month annualized, and revision-adjusted changes.

## Indicator Classification

Use this map as a starting point, then adjust by regime.

| Area | Level / Stock | First-Derivative Signals | Second-Derivative Signals |
| --- | --- | --- | --- |
| Bank liquidity | Discount-window primary/secondary credit, SRF usage, reserve balances | Primary credit rising week-over-week; reserves falling; SRF take-up appears | Primary credit rise accelerates; secondary credit appears; SRF and discount window rise together; bank spreads/equities deteriorate simultaneously |
| Money-market plumbing | SOFR-IORB, EFFR-IORB, repo rates, ON RRP, TGA | SOFR-IORB moves toward zero; repo rates rise; ON RRP drains; TGA rebuilds | SOFR-IORB turns positive outside quarter-end; repo spikes repeat; ON RRP is low while TGA rises and reserves fall |
| Treasury liquidity | Bid-ask, auction tails, dealer takedown, term premium, MOVE | Auction tails widen; dealer take-down rises; term premium rises | Weak auctions cluster; term premium and MOVE accelerate; Treasury selloff spills into equities/credit |
| Credit | IG/HY spreads, CDS, bank funding spreads, commercial paper | Spreads widen over 5-20 days; issuance quality weakens | Spread widening accelerates; lower-quality credit gaps wider; issuance window closes; downgrades/default fears rise |
| Equities | VIX, skew, market breadth, leadership, bank/financials relative strength | VIX rises; breadth deteriorates; financials underperform | VIX and credit spreads rise together; bank underperformance accelerates; equity weakness stops being narrow |
| Labor | Unemployment, claims, payroll breadth, hours, revisions | Claims rise; payroll breadth narrows; hours fall; revisions turn negative | Deterioration accelerates across claims, unemployment, hours, and revisions; layoffs spread from cyclicals to services |
| Inflation | Core services, supercore proxy, wages, breakevens | 3-month annualized inflation/wage momentum changes direction | Inflation and wages re-accelerate together, or disinflation accelerates with labor weakness |
| Fiscal supply | QRA, coupon supply, bill share, TGA path, deficit surprises | Borrowing estimates rise; coupon share rises; TGA rebuild drains reserves | Supply shocks coincide with weak auctions, rising term premium, and liquidity-drain plumbing pressure |

## Early-Warning Rules

Treat a single first-derivative signal as a watch item, not a crisis call. Upgrade the warning only when signals cluster.

### Yellow warning

Use when at least two conditions hold:

- One plumbing variable deteriorates for 2-3 observations.
- A stress variable rises from a low base faster than its recent norm.
- The level is not extreme, but the direction is persistent.
- Market transmission is still limited.

Examples:

- Primary credit rises for several weeks, but secondary credit is zero and SOFR-IORB remains contained.
- ON RRP drains while reserves are still ample.
- Credit spreads widen modestly, but VIX and bank equities do not confirm.

### Orange warning

Use when first-derivative deterioration is joined by second-derivative acceleration:

- The same stress variable worsens faster than the prior window.
- Adjacent markets begin confirming the same direction.
- Policy-sensitive spreads or plumbing indicators move together.
- Market pricing begins to reflect forced de-risking rather than normal repricing.

Examples:

- Primary credit rise accelerates while bank equities weaken and bank CDS/funding spreads widen.
- SOFR-IORB turns positive repeatedly while repo stress and SRF usage appear.
- Auction tails widen while term premium and MOVE rise together.

### Red warning

Use when level, first derivative, and second derivative are all adverse:

- Absolute level is near prior stress regimes or policy-response thresholds.
- Deterioration is persistent and accelerating.
- Transmission has crossed at least three areas, such as banks, repo, Treasuries, credit, and equities.
- Central-bank facilities or emergency tools become the main market focus.

Examples:

- Discount-window borrowing reaches stress-regime levels, secondary credit appears, SRF usage rises, bank spreads widen, and SOFR-IORB remains positive.
- Treasury-market dysfunction forces official liquidity operations while credit spreads and equity volatility accelerate.

## Transmission-Chain Mapping

When explaining a crisis path, present it as a chain rather than a list:

```text
Trigger -> funding/plumbing stress -> balance-sheet constraint -> asset sales / hedging -> market volatility -> credit tightening -> real-economy feedback -> policy response
```

Common chains:

| Chain | Early First-Derivative Clue | Second-Derivative Confirmation |
| --- | --- | --- |
| Reserve scarcity chain | ON RRP low, TGA rising, reserves falling | SOFR-IORB positive, repo spikes repeat, SRF usage grows |
| Bank funding chain | Primary credit rises from low base | Primary credit acceleration, secondary credit appears, bank spreads/equities deteriorate |
| Treasury supply chain | Auction tails widen, dealer takedown rises | Term premium and MOVE accelerate, weak auctions cluster, equities/credit react |
| Recession chain | Claims and unemployment trend higher | Payroll breadth, hours, revisions, credit spreads, and earnings breadth weaken together |
| Inflation re-acceleration chain | 3-month annualized core/wage momentum rises | Breakevens, front-end rates, and Fed communications reprice in the same direction |

## Scoring

Score each major area separately:

| Score | Meaning |
| ---: | --- |
| 0 | No meaningful stress; levels and derivatives benign. |
| 1 | One first-derivative warning, not yet confirmed. |
| 2 | Persistent first-derivative warning or mild cross-market confirmation. |
| 3 | Second-derivative acceleration appears in one chain. |
| 4 | Acceleration spreads across two or more chains. |
| 5 | Level, first derivative, and second derivative all indicate crisis pressure. |

Do not average away plumbing stress. If bank-funding or repo plumbing reaches 4-5, explicitly state that it can override otherwise benign inflation/labor readings for short-horizon risk management.

## Output Add-On

When this reference applies, add a compact derivative dashboard:

```text
Level: benign / stretched / stress-regime
First derivative: improving / stable / deteriorating
Second derivative: decelerating / neutral / accelerating
Transmission chain: not started / localized / cross-market / systemic
Policy-response likelihood: low / medium / high
```

Then separate:

- What has already happened.
- What is deteriorating at the margin.
- What would confirm acceleration.
- Which market would likely transmit stress next.

Avoid deterministic language. A second-derivative warning raises crisis probability; it does not prove the crisis has arrived.
