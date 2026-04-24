---
name: hermes-langmem-memory-architecture-upgrade
description: Upgrade Hermes' existing LangMem provider from basic memory wiring into a deliberate multi-lane memory architecture with typed profile storage, provenance metadata, debounced sync, reranked retrieval, episodic memory, an eval harness, and a reviewed procedural-memory loop.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, langmem, memory, sqlite, evaluation, prompt-review, architecture]
    related_skills: [hermes-langmem-provider-iteration, test-driven-development, writing-plans, hermes-agent]
---

# Hermes LangMem memory architecture upgrade

Use this when a Hermes repo already has the LangMem provider wired in and you want to upgrade it into a more structured, inspectable, and testable memory system. It is written to be shareable across Hermes installs, not tied to one local machine.

## What this skill upgrades

This pattern turns Hermes memory from a basic LangMem integration into a local multi-lane architecture with:

- typed profile memory for durable user facts
- explicit provenance metadata on memory rows
- debounced background extraction
- lightweight retrieval reranking without changing backend
- a separate episodic lane for reusable successful interaction patterns
- a deterministic eval harness
- a reviewed procedural-memory loop stub that does not auto-patch prompts

## When to use

Use this when you need one or more of these outcomes:

- stable user preferences should not depend on lexical search
- memory rows need provenance, confirmation counts, and debug visibility
- `sync_turn()` is too eager and noisy
- retrieval quality is weak but you do not want embeddings or new infrastructure yet
- reusable success patterns should be stored separately from user facts
- memory quality needs deterministic local evaluation
- prompt optimization should be reviewed instead of automatic

## Repo assumptions

This skill assumes a Hermes repo with the bundled LangMem provider and a layout roughly like:

- `plugins/memory/langmem/__init__.py`
- `plugins/memory/langmem/store.py`
- `tests/agent/test_langmem_provider.py`
- `tests/agent/test_langmem_store.py`

Optional files created by this upgrade:

- `tests/agent/test_langmem_profile_lane.py`
- `tests/agent/test_langmem_episodic_lane.py`
- `tests/integration/test_langmem_eval.py`
- `scripts/langmem_prompt_review.py`
- `docs/plans/...`

## Important preflight checks

1. Confirm the repo already has a LangMem provider seam.
2. Check whether the worktree is noisy before claiming a clean commit path.

```bash
cd /path/to/your/hermes-agent-repo
git status --short
```

If the worktree is dirty, do not promise a clean isolated commit until you explicitly isolate the intended files.

## Upgrade order

Apply these in order:

1. typed profile lane
2. metadata and provenance
3. debounced background extraction
4. retrieval reranking
5. episodic lane
6. deterministic eval harness
7. reviewed procedural-memory workflow stub

Do not skip ahead. Later steps depend on earlier structure.

## Task 1: Typed profile lane

Add a stable profile schema and direct profile storage so enduring user facts are not just free-text rows.

### Files
- Modify: `plugins/memory/langmem/__init__.py`
- Modify: `plugins/memory/langmem/store.py`
- Modify: `tests/agent/test_langmem_provider.py`
- Create: `tests/agent/test_langmem_profile_lane.py`

### Required behavior
- define `HermesUserProfile`
- add `_get_profile_manager()`
- add `get_profile(user_id)` and `upsert_profile(user_id, profile, session_id=...)`
- make `langmem_profile` return direct structured profile first
- fall back to legacy memory listing only when no profile exists
- feed typed profile extraction during background sync

### Verification
```bash
pytest tests/agent/test_langmem_profile_lane.py -q
pytest tests/agent/test_langmem_provider.py tests/agent/test_langmem_profile_lane.py -q
```

## Task 2: Metadata and provenance

Add explicit metadata so every row is easier to debug, rank, and evaluate.

### Files
- Modify: `plugins/memory/langmem/__init__.py`
- Modify: `plugins/memory/langmem/store.py`
- Modify: `tests/agent/test_langmem_store.py`
- Modify: `tests/agent/test_langmem_provider.py`

### Required behavior
- centralize metadata creation with `_build_metadata()`
- centralize merge behavior with `_merge_metadata()`
- preserve `first_seen_session_id`
- update `last_seen_session_id`
- increment `confirmation_count`
- enrich explicit conclude writes, background sync rows, and profile persistence

### Recommended metadata fields
- `lane`
- `source_type`
- `first_seen_session_id`
- `last_seen_session_id`
- `confirmation_count`
- `tags`

## Task 3: Debounced sync

Make `sync_turn()` buffer rapid turns and only process the latest payload.

### Files
- Modify: `plugins/memory/langmem/__init__.py`
- Modify: `tests/agent/test_langmem_provider.py`

### Required behavior
- add config like `debounce_seconds`
- keep pending sync payload, deadline, and lock state
- move immediate sync work into `_run_single_sync()`
- let rapid repeated calls overwrite the pending payload
- process only the latest payload once the debounce window expires

### Verification
```bash
pytest tests/agent/test_langmem_provider.py -q -k debounce
```

## Task 4: Retrieval reranking

Improve local recall without changing storage backend.

### Files
- Modify: `plugins/memory/langmem/store.py`
- Modify: `tests/agent/test_langmem_store.py`

### Required behavior
- add `_score_row()`
- score using local metadata, starting with:
  - `confirmation_count`
  - `updated_at` recency bonus
- rerank Python-side after both FTS5 and LIKE fallback
- keep `langmem_profile` direct and non-search-based

### Verification
```bash
pytest tests/agent/test_langmem_store.py -q -k search
```

## Task 5: Episodic lane

Store reusable successful interaction patterns separately from user facts.

### Files
- Modify: `plugins/memory/langmem/__init__.py`
- Create: `tests/agent/test_langmem_episodic_lane.py`

### Required behavior
- define `HermesEpisode`
- add `_get_episode_manager()`
- gate writes with a simple explicit success heuristic
- persist episodes with:
  - `kind="episode"`
  - `source="langmem-episode"`
  - metadata lane `episodes`
  - metadata source type `episode_sync`
- keep episode payloads JSON-encoded so SQLite stays inspectable

### Simple heuristic that worked well
- require non-empty user and assistant content
- skip very short or obviously transactional user turns
- skip assistant replies containing failure markers like `error`, `failed`, `unable`, `cannot`, `refused`, `missing dependency`

### Verification
```bash
pytest tests/agent/test_langmem_episodic_lane.py -q
pytest tests/agent/test_langmem_store.py tests/agent/test_langmem_provider.py tests/agent/test_langmem_profile_lane.py tests/agent/test_langmem_episodic_lane.py -q
```

## Task 6: Deterministic eval harness

Add a local regression harness that scores memory behavior in separable layers.

### Files
- Create: `tests/integration/test_langmem_eval.py`
- Create: `docs/plans/2026-04-24-langmem-eval-rubric.md`

### Scenario families
- explicit preference writes
- preference correction / supersession
- cross-session recall
- retrieval under lexical ambiguity

### Score dimensions
- `extraction_score`
- `reconciliation_score`
- `retrieval_score`
- `injection_usefulness_score`

### Required artifact
- `tmp/langmem-eval/latest.json`

### Important pytest gotcha
This repo excludes integration tests by default in `pyproject.toml`.
Use:

```bash
pytest -q -m integration tests/integration/test_langmem_eval.py
```

Do not rely on `pytest tests/integration/test_langmem_eval.py -q` alone in repos that default to `-m 'not integration'`.

## Task 7: Reviewed procedural-memory workflow stub

Add a scaffold for prompt-learning review without auto-patching the live system prompt.

### Files
- Create: `scripts/langmem_prompt_review.py`
- Create: `docs/plans/2026-04-24-langmem-procedural-memory-loop.md`

### Required behavior
The first version should:
- load failed trajectories from JSON
- summarize failures by category
- emit a review packet to `tmp/langmem-prompt-review/latest.json`
- explicitly mark where `create_prompt_optimizer` would run later
- never auto-apply prompt changes

### Verification
```bash
python scripts/langmem_prompt_review.py --help
python scripts/langmem_prompt_review.py --input tmp/langmem-prompt-review-sample.json
```

## Final verification pass

Run this focused suite after the upgrade:

```bash
pytest tests/agent/test_langmem_provider.py tests/agent/test_langmem_store.py tests/agent/test_langmem_profile_lane.py tests/agent/test_langmem_episodic_lane.py -q
pytest -q -m integration tests/integration/test_langmem_eval.py
```

### Typical warning noise
You may still see upstream/dependency warnings from:
- LangGraph / `trustcall` deprecations
- Anthropic deprecation for `claude-3-5-haiku-latest`

Treat those as dependency noise unless functionality regresses.

## What this skill does not do

- does not replace the Hermes provider seam
- does not require hosted infra
- does not add embeddings first
- does not auto-delete on omission
- does not use search as a substitute for typed profile lookup
- does not auto-patch the live prompt from optimizer output

## What to inspect locally after rollout

- profile row exists in SQLite after a few turns
- explicit conclude facts persist
- metadata JSON includes lane/source/session fields
- search results are user-scoped and sensibly ranked
- episode rows live in their own lane
- `tmp/langmem-eval/latest.json` is generated cleanly
- `tmp/langmem-prompt-review/latest.json` is generated cleanly

## Support files in this skill

Read these linked files too:
- `references/architecture.md`
- `references/test-matrix.md`
- `templates/langmem-eval-rubric.md`
- `templates/langmem-procedural-memory-loop.md`

## Bottom line

This is a memory-discipline upgrade, not just a memory feature toggle. It gives Hermes a structured, inspectable, locally testable LangMem architecture.
