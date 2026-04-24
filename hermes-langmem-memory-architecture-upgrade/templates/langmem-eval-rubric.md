# LangMem eval rubric for Hermes

## Score dimensions

- `extraction_score`
- `reconciliation_score`
- `retrieval_score`
- `injection_usefulness_score`

## Scenario families

1. explicit preference writes
2. preference correction / supersession
3. cross-session recall
4. retrieval under lexical ambiguity

## Interpretation

### Extraction score
Was the expected durable fact or row actually created?

### Reconciliation score
Was old state preserved, superseded, merged, or retired correctly?

### Retrieval score
Did search or direct lookup return the right memory?

### Injection usefulness score
Would the retrieved output actually help the next turn, or would it mislead the assistant?

## Failure reading guide

| Pattern | Likely problem |
|---|---|
| extraction low | write path broken |
| extraction high, reconciliation low | merge/delete/session metadata logic broken |
| extraction + reconciliation high, retrieval low | ranking or lookup path broken |
| retrieval high, injection usefulness low | provider formatting or presentation broken |

## Guardrails

- keep the baseline deterministic
- prefer store/provider assertions over fuzzy judgments
- use evals to localize failures before adding infrastructure
