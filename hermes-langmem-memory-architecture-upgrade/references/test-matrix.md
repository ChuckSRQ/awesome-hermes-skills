# Hermes LangMem upgrade test matrix

## Focused rollout order

### Task 1: profile lane
```bash
pytest tests/agent/test_langmem_profile_lane.py -q
pytest tests/agent/test_langmem_provider.py tests/agent/test_langmem_profile_lane.py -q
```

Proves:
- typed profile lookup works
- fallback behavior still works

### Task 2: metadata and provenance
```bash
pytest tests/agent/test_langmem_store.py tests/agent/test_langmem_provider.py tests/agent/test_langmem_profile_lane.py -q
```

Proves:
- metadata writes and merges work
- confirmation/session provenance fields behave correctly

### Task 3: debounce
```bash
pytest tests/agent/test_langmem_provider.py -q -k debounce
```

Proves:
- rapid sync calls collapse into one extraction pass
- latest payload wins

### Task 4: reranking
```bash
pytest tests/agent/test_langmem_store.py -q -k search
```

Proves:
- confirmed memories outrank single-seen duplicates
- recent memories outrank stale matches when text is otherwise equal

### Task 5: episodic lane
```bash
pytest tests/agent/test_langmem_episodic_lane.py -q
pytest tests/agent/test_langmem_store.py tests/agent/test_langmem_provider.py tests/agent/test_langmem_profile_lane.py tests/agent/test_langmem_episodic_lane.py -q
```

Proves:
- successful patterns are stored in a separate lane
- error turns do not create episodes

### Task 6: eval harness
```bash
pytest -q -m integration tests/integration/test_langmem_eval.py
```

Proves:
- deterministic scenario families pass
- eval artifact is written to `tmp/langmem-eval/latest.json`

### Task 7: procedural-memory scaffold
```bash
python scripts/langmem_prompt_review.py --help
python scripts/langmem_prompt_review.py --input tmp/langmem-prompt-review-sample.json
```

Proves:
- CLI is usable
- review packet can be generated

## Final focused suite
```bash
pytest tests/agent/test_langmem_provider.py tests/agent/test_langmem_store.py tests/agent/test_langmem_profile_lane.py tests/agent/test_langmem_episodic_lane.py -q
pytest -q -m integration tests/integration/test_langmem_eval.py
```

## Important pytest gotcha
If the repo sets default `addopts` to exclude integration tests, direct invocation like this may report no tests ran:

```bash
pytest tests/integration/test_langmem_eval.py -q
```

Use:

```bash
pytest -q -m integration tests/integration/test_langmem_eval.py
```

## Expected warning noise
These warnings can still appear without indicating functional failure:
- LangGraph / `trustcall` deprecation warnings
- Anthropic deprecation warning for `claude-3-5-haiku-latest`

## Manual spot checks
After the focused suite passes, inspect:

```bash
sqlite3 ~/.hermes/langmem.sqlite3 'select id,user_id,kind,content,metadata_json from memories order by updated_at desc limit 20;'
```

Verify:
- a profile row exists
- explicit facts persist
- metadata JSON contains lane/source/session info
- episode rows are in their own lane
