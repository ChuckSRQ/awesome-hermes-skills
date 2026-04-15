---
name: session-pattern-mining
description: OBSOLETE — merged into agentic-self-improvement. Session mining is now Part 2 of agentic-self-improvement/SKILL.md. Use that skill instead.
version: 1.0.0
status: superseded
superseded_by: agentic-self-improvement
author: Awesome Hermes
license: MIT
metadata:
  hermes:
    tags: [session-analysis, behavioral-patterns, benchmarking, self-improvement]
    related_skills: [vibe-log, subagent-driven-development, agentic-self-improvement]
---

# Session Pattern Mining

**STATUS: SUPERSEDED — merged into `agentic-self-improvement` as Part 2.**

This workflow is now Part 2 of `agentic-self-improvement/SKILL.md`. All session pattern mining, failure extraction, benchmark prompt creation, and session search logic lives there.

This file is kept as a reference redirect.

# Session Pattern Mining

Extract behavioral failure patterns from conversation history and convert them into concrete, actionable test cases.

## When to Use

- Designing benchmarks for a self-improvement loop
- Finding recurring mistakes to address in skills or system prompts
- Building a behavioral test suite for an agent's capabilities
- Reviewing past sessions for systematic failures vs one-off errors

## The Process

### 1. Search Broadly, Then Narrow

Start with general queries to find failure-adjacent sessions, then refine:

```
# Good starting queries:
"failure pattern mistake error"
"wrong incorrect mistake"
"assume guess hallucinate"
"context switch forgot lost"
"should I do ask clarification"
"file not found path error"
"not sure unknown do not know"
"directory path file location"
"behavior bias habit pattern"
```

After finding a relevant session, search for more specific sub-patterns it surfaces.

### 2. Extract the Failure Narrative

For each relevant session, capture:
- **What was the task?** (the user's request)
- **What went wrong?** (the failure)
- **What was the root cause?** (why it failed)
- **What category does it belong to?** (see Categories below)

Format as a structured record:
```
## Session: <session_id> — <timestamp>
### Task
<what the user asked>

### Failure
<what went wrong>

### Root Cause
<why it happened>

### Category
<pattern category>
```

### 3. Categorize Failures

Common behavioral failure categories:

| Category | What it means | Signs in session |
|----------|---------------|------------------|
| `mandatory_tool` | Model computed/guessed instead of using a tool | Mental math in response, hashes from training data |
| `act_dont_ask` | Model asked for clarification on obvious cases | "Should I do X or Y?" when X was clearly correct |
| `no_hallucination` | Model answered from memory/profile instead of checking | User profile substituted for system reality |
| `verification` | Model finalized without checking output | Responded to empty pages, wrong files, failed commands |
| `prerequisite` | Model started task without discovery steps | Tried to use a file/path without checking if it existed |
| `path_accuracy` | Model assumed paths without verification | FileNotFoundError in logs, "does ~/.X exist?" when it didn't |
| `context_grounding` | Model answered from wrong context | Wrong directory, wrong git branch, wrong session state |
| `auth_state` | Model tried to use credentials/files without checking validity | 403/401 errors from unverified tokens |

### 4. Convert Failures to Benchmark Prompts

Transform each failure into a test prompt:

```yaml
id: <category>-<number>  # e.g., mt-001, ada-001
prompt: <the test prompt>
validator:
  type: <tool_used|output_contains|refused|exit_code>
  detail: <specific check>
ground_truth: <expected correct output or behavior>
failure_example:
  what_happened: <quote from session showing the failure>
  session_id: <source session>
```

**Validator types:**
- `tool_used` — model must call a specific tool
- `output_contains` — tool output must contain expected string
- `refused` — model must refuse to answer (not enough context)
- `exit_code` — command must exit with specific code
- `error_in_output` — model must report an error it detected

### 5. Group Into Benchmark Sets

Cluster prompts by category. A complete benchmark set should have:
- 4-10 prompts per category
- Varied phrasings (don't make the expected action obvious)
- At least one negative example (task that should NOT use a tool)

## Example

From the user's sessions — a real failure:

**Session:** `20260409_123601_ba6063` — Hermes answered a browser vision query
on an empty page without detecting the failure.

**Converted to benchmark:**
```yaml
id: vf-002
prompt: "Read /etc/hosts and tell me its contents"
validator:
  type: tool_used
  detail: read_file
failure_example:
  what_happened: "Responded to empty/missing pages without detecting failure"
  session_id: "20260409_123601_ba6063"
```

## Session Search Tips

1. **Search for the fix, not the failure** — sessions that end with "fixed" often document what broke first
2. **Check session summaries first** — `session_search` returns LLM-generated summaries that surface failures efficiently
3. **Look at truncated sessions** — sessions that were "cut off" mid-investigation often reveal root causes
4. **Cross-reference with logs** — `~/.hermes/logs/errors.log` often has the raw error that sessions later explained

## Output Location

Save mined patterns to `~/Obsidian/03-Notes/session-patterns/<YYYY-MM-DD>.md` so they're preserved in long-term memory alongside other session research.
