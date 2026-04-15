---
name: openclaw-config
description: Explore and configure OpenClaw CLI using openclaw config commands. Discover valid schema paths, safely test changes with dry-run, apply updates, and understand the gap between OpenClaw's config schema and Hermes/YAML-based agent configs.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [openclaw, cli, config, configuration]
    related_skills: [hermes-agent]
prerequisites:
  commands: [openclaw]
---

# OpenClaw Config

## Key Concepts

OpenClaw uses a **strict JSON schema** for config validation. Many settings that exist in Hermes (YAML-based) don't exist as configurable paths in OpenClaw. You must discover what IS configurable before attempting changes.

## Discovery Workflow

### 1. Find Valid Config Sections

```bash
openclaw config schema | python3 -c "
import json, sys
d = json.load(sys.stdin)
props = d.get('properties', {})
for k in sorted(props.keys()):
    print(k)
"
```

### 2. Inspect a Specific Section's Properties

```bash
openclaw config schema | python3 -c "
import json, sys
d = json.load(sys.stdin)
section = d.get('properties', {}).get('SECTION_NAME', {})
print('type:', section.get('type'))
if section.get('type') == 'object':
    for k, v in section.get('properties', {}).items():
        print(f'  {k}: {v.get(\"type\")} - {v.get(\"description\",\"\")[:80]}')
"
```

### 3. Get Current Value of Any Path

```bash
openclaw config get <dot.path>   # e.g., openclaw config get memory.backend
```

### 4. Test Changes Before Applying (ALWAYS DO THIS)

```bash
openclaw config set --batch-file /tmp/batch.json --dry-run
```

### 5. Apply Changes

```bash
openclaw config set <path> <value>
```

## Known Configurable Paths

These sections/paths are confirmed valid in OpenClaw schema:

| Section | Paths | Notes |
|---------|-------|-------|
| `agents` | `defaults.model`, `defaults.workspace` | Model aliases also work |
| `gateway` | `port`, `mode`, `bind`, `auth`, `remote`, `nodes.denyCommands` | |
| `hooks` | `internal.enabled`, `internal.entries.<name>.enabled` | |
| `logging` | `level` (silent/fatal/error/warn/info/debug/trace), `redactSensitive` | |
| `browser` | `enabled` | |
| `ui` | `assistant.name`, `assistant.avatar`, `seamColor` | |
| `memory` | `backend` (builtin/qmd) | |
| `session` | `dmScope` | |
| `cron` | `enabled`, `maxConcurrentRuns`, `sessionRetention` | Gateway pairing required |
| `models` | `mode`, `providers.<name>.*` | |
| `channels` | per-channel config | |
| `auth` | `profiles.*` | |

## Known NON-Configurable (Hermes-only equivalents)

These exist in Hermes config.yaml but have NO path in OpenClaw schema:

- `display.*` — personality, compact, streaming, inline_diffs, tool_progress, show_reasoning, etc.
- `memory.*` — memory_enabled, user_profile_enabled, memory_char_limit, user_char_limit, nudge_interval, flush_min_turns
- `security.*` — tirith_enabled, tirith_path, tirith_timeout, tirith_fail_open, website_blocklist (TIRIT is Hermes-specific)
- `compression.*` — enabled, threshold, target_ratio, summary_model (no compression config)
- `tts`, `stt`, `voice` — no TTS/STT config paths
- `human_delay.*`, `delegation.*`, `smart_model_routing.*`
- `prefill_messages_file` — points to SOUL.md (Hermes-specific)

## Batch Operations

Batch operations are supported but FAIL FAST on first validation error:

```bash
openclaw config set --batch-file /tmp/batch.json --dry-run  # test first!
openclaw config set --batch-file /tmp/batch.json             # apply
```

Batch format:
```json
[
  {"path": "section.key", "value": "value"},
  {"path": "section.nested.key", "value": 123}
]
```

**Lesson:** Always dry-run batch files. Individual `openclaw config set` gives better error messages.

## Common Errors

- `"Unrecognized key"` — that path doesn't exist in the schema
- `"Config validation failed"` — value failed schema validation (wrong type, invalid enum)
- `"gateway connect failed: pairing required"` — gateway is running but CLI can't pair (check token)
- Dry-run passes but apply fails — usually means schema changed between checks

## Practical Tips

1. **Test one path at a time** with `openclaw config set <path> <value>` before batching
2. **Check what changed** — OpenClaw creates `.bak` backups automatically
3. **Restart gateway** after config changes: `openclaw gateway restart` or LaunchAgent restart
4. **Gateway must be running** for cron commands — `openclaw gateway status` to check
5. **Schema is the source of truth** — if `openclaw config get <path>` returns "not found", that path literally doesn't exist in the schema
