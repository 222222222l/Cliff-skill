# Causal extension — integration notes

The causal extension is installed in this Skill's tree when these paths exist:

- `references/political-economy-causal-engine.md`: competing hypotheses, macro–micro causal identification, adversarial checks.
- `evals/cases.md`: eight evaluation cases for revisions and regression testing.
- `SKILL.md` section `Causal Identification and Macro–Micro Coherence`: activation rule and brief guidelines.

The original integration patch instructions are preserved below for maintainers, but are already reflected in the added files and Skill header. For future edits, run the eight evaluation cases and compare subsequent real outcomes against dated predictions.

---

# Proposed integration into China-policy-analysis-skill

This is an additive, **uncommitted** patch package. The existing repository files are unchanged.

Copy:
- `references/political-economy-causal-engine.md` → `China-policy-analysis-skill/references/`
- `evals/cases.md` → `China-policy-analysis-skill/evals/`

Then append this short section to the **existing** `SKILL.md`, near its `Analysis Workflow` heading:

```markdown
## Causal Identification and Macro–Micro Coherence

For analyses of reform motivation, political constraints, central-local
implementation, policy conflict, or macro-to-household transmission, read
`references/political-economy-causal-engine.md`.

Treat the political-economy hierarchy in `Core Stance` as a set of contestable
hypotheses rather than a universally established ranking. Test at least three
competing explanations when hidden intentions are material: political/security
constraints, fiscal/financial constraints, principal-agent/implementation
capacity, and/or development/welfare trade-offs.

Always link: objective and authority → funding or enforcement → institutions'
choices → industry balance sheets and prices → household cash flow, risk and
exit rights → macro feedback. Identify counterevidence, one differentiating
prediction and a condition under which the preferred explanation would fail.

For official data, preserve publication versions and flag delayed, withdrawn,
or methodology-changed releases—especially after deterioration—without treating
them as automatic proof of manipulation.

Use heuristic scores and first/second derivatives as descriptive monitoring,
not calibrated default or crisis probabilities. When recommending household
actions, weigh the opportunity cost of excessive caution alongside tail risks.
```

Optional improvement: in `Core Stance`, replace the phrase 'Use the following political-economy hypotheses as a starting frame unless the user states another' with 'Treat the following as one candidate political-economy hierarchy; use alongside competing fiscal, developmental, implementation, and security explanations, and never let the hierarchy decide the conclusion before evidence is examined.'

Run the eight evaluation cases after future prompt/tool revisions. Save past predictions and later observed outcomes for out-of-sample calibration.