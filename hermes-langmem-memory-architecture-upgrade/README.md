# hermes-langmem-memory-architecture-upgrade

A shareable Hermes skill for upgrading the bundled LangMem provider from a basic memory hookup into a structured local memory architecture.

## Why this exists

Hermes can already wire in LangMem, but basic memory enablement is not the same thing as a disciplined memory architecture.

This skill packages a practical upgrade path for Hermes users who want memory to become:
- more structured
- more inspectable
- easier to test locally
- safer to evolve over time

## What it adds

This skill walks a Hermes repo through:

- a typed profile lane for stable user facts
- provenance-aware metadata on memory rows
- debounced background extraction
- lightweight retrieval reranking using local metadata
- a separate episodic lane for reusable successful interaction patterns
- a deterministic evaluation harness
- a reviewed procedural-memory workflow stub for prompt optimization

## What it does not try to do

This is intentionally **not**:
- a drop-in Python package
- a hosted memory backend
- an embeddings-first redesign
- an auto-patching prompt optimizer

It is an implementation recipe for improving the bundled Hermes LangMem provider in place.

## Repo contents

- `SKILL.md` — main implementation skill
- `references/architecture.md` — architecture overview and lane model
- `references/test-matrix.md` — focused verification commands and what they prove
- `templates/langmem-eval-rubric.md` — reusable eval rubric
- `templates/langmem-procedural-memory-loop.md` — reusable reviewed prompt-memory policy template

## Assumptions

This skill assumes:
- you already have a Hermes repo
- that repo already includes the bundled LangMem provider
- you want to improve the existing provider seam rather than replace it

## Install

Copy this repo or just the skill directory into:

```bash
~/.hermes/skills/software-development/hermes-langmem-memory-architecture-upgrade/
```

Then load the skill by name:

```text
hermes-langmem-memory-architecture-upgrade
```

## Verification flow

Typical focused verification after applying the upgrade:

```bash
pytest tests/agent/test_langmem_provider.py tests/agent/test_langmem_store.py tests/agent/test_langmem_profile_lane.py tests/agent/test_langmem_episodic_lane.py -q
pytest -q -m integration tests/integration/test_langmem_eval.py
python scripts/langmem_prompt_review.py --help
```

## Best fit

This is best for technical Hermes users who want a stronger memory system without jumping straight to new infrastructure.

## License

MIT
