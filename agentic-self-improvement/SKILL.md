---
name: agentic-self-improvement
description: Run behavioral benchmarks against the agent, detect failure patterns, generate guidance patches, apply them with auto-revert safety net. Implements the closed-loop self-improvement cycle from Hermes PR #6120, extended with GEPA-style evolutionary optimization and session mining.
version: 2.0.0
author: Hermes Community
license: MIT
metadata:
  hermes:
    tags: [self-improvement, behavioral-benchmarking, guidance-patch, closed-loop, evolutionary-optimization, GEPA, DSPy]
    related_skills: []
  evolution:
    homepage: https://github.com/NousResearch/hermes-agent-self-evolution
    stars: 1600+
    license: MIT
---

# Agentic Self-Improvement Loop

Behavioral benchmarking + evolutionary self-improvement for Hermes Agent. Combines closed-loop guidance patching (from Hermes PR #6120) with the GEPA optimization framework from `hermes-agent-self-evolution` (NousResearch, MIT).

---

## Core Loop

```
BENCHMARK → DIAGNOSE → PATCH → VERIFY → (auto-revert if regression)
                    ↓
              GEPA OPTIMIZE → EVAL DATASET → EVOLVE → DEPLOY
                    ↓
              SESSION MINE → LLM-AS-JUDGE → NEW BENCHMARKS
```

**Two modes operate together:**
- **Guidance Patch Loop** — fast, surgical, targets specific behavioral failures via guidance blocks
- **Evolutionary Optimization Loop** — principled, uses GEPA + DSPy to optimize skill text end-to-end

---

## Part 1: Guidance Patch Loop

### Core Loop

```
BENCHMARK → DIAGNOSE → PATCH → VERIFY → (auto-revert if regression)
```

### Usage

```bash
# Run all benchmarks, show suggested patches (no changes made)
/self-improve

# Run all benchmarks, auto-apply if improvement, auto-revert if regression
/self-improve --mode=apply

# Run specific category only
/self-improve --benchmarks=mandatory_tool.yaml

# Run subset of categories
/self-improve --categories=mandatory_tool,act_dont_ask,no_hallucination

# Test a specific model
/self-improve --model=claude-sonnet-4

# Control parallelism (default: 4)
/self-improve --parallel=8

# View past results
/self-improve --view-results=2026-04-12_1400

# Revert last applied patch
/self-improve --revert
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `suggest` | `suggest` (show diff only) or `apply` (apply + verify) |
| `--benchmarks` | all | Benchmark YAML file(s) to run |
| `--categories` | all | Run only specific categories (by filename without .yaml) |
| `--model` | current | Model to benchmark |
| `--parallel` | 4 | Number of parallel prompt executions |
| `--view-results` | none | Show a past run's results |
| `--revert` | false | Revert the last applied patch |

### Benchmark Categories

| Category | File | What it tests |
|----------|------|---------------|
| `mandatory_tool` | `BENCHMARKS/mandatory_tool.yaml` | Must use tools for math/hashes/time/files |
| `act_dont_ask` | `BENCHMARKS/act_dont_ask.yaml` | Act on obvious interpretation, don't ask |
| `no_hallucination` | `BENCHMARKS/no_hallucination.yaml` | Check system, don't answer from profile/memory |
| `verification` | `BENCHMARKS/verification.yaml` | Verify outputs before finalizing |
| `prerequisite` | `BENCHMARKS/prerequisite.yaml` | Discover before acting |
| `path_accuracy` | `BENCHMARKS/path_accuracy.yaml` | Verify paths before using |
| `context_grounding` | `BENCHMARKS/context_grounding.yaml` | Check actual context, don't assume |
| `auth_state` | `BENCHMARKS/auth_state.yaml` | Verify credentials before using them |
| `remember_to_obsidian` | `BENCHMARKS/remember_to_obsidian.yaml` | Write durable facts to Obsidian, not just memory tool |

### How the Guidance Patch Loop Works

**1. Benchmark Runner**

Each prompt runs in isolation via `hermes chat --model <model> -q QUERY -Q` as a subprocess. Captures:
- Tool calls made (detected as "preparing X..." text previews in quiet mode)
- Tool outputs
- Final response text
- Exit code

**2. Failure Analyzer**

Groups failures by category, computes per-category pass rates, extracts failure examples.

**3. Patch Generator**

Generates XML guidance blocks for the relevant model type:
- OpenAI/GPT/Codex → `OPENAI_MODEL_EXECUTION_GUIDANCE`
- Anthropic/Claude → `ANTHROPIC_MODEL_EXECUTION_GUIDANCE`
- Google/Gemini → `GEMINI_MODEL_EXECUTION_GUIDANCE`
- MiniMax → `MINIMAX_MODEL_EXECUTION_GUIDANCE`

**4. Apply + Verify + Auto-Revert**

**Suggest mode:** Shows the diff, writes to `~/.hermes/self-improvement/proposed_patches/<run_id>.diff`

**Apply mode:**
1. Run baseline benchmarks → capture pass rates
2. Backup `prompt_builder.py` to `~/.hermes/self-improvement/backups/<timestamp>/`
3. Apply patch to relevant GUIDANCE constant
4. Re-run benchmarks → compare pass rates
5. If ANY category regresses → auto-revert to backup
6. If all improve → keep patch, report delta

### Output Locations

| What | Where |
|------|-------|
| Benchmark results | `~/.hermes/self-improvement/results/<run_id>/` |
| Proposed patches | `~/.hermes/self-improvement/proposed_patches/<run_id>.diff` |
| Backups | `~/.hermes/self-improvement/backups/<timestamp>/` |
| Logs | `~/.hermes/logs/` |

---

## Part 2: Session Pattern Mining

Extract behavioral failure patterns from conversation history and convert them into concrete, actionable test cases.

### When to Use

- Designing benchmarks for a self-improvement loop
- Finding recurring mistakes to address in skills or system prompts
- Building a behavioral test suite for an agent's capabilities
- Reviewing past sessions for systematic failures vs one-off errors

### The Process

**1. Search Broadly, Then Narrow**

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

**2. Extract the Failure Narrative**

For each relevant session:
- **What was the task?** (the user's request)
- **What went wrong?** (the failure)
- **What was the root cause?** (why it failed)
- **What category does it belong to?** (see Categories below)

```markdown
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

**3. Categorize Failures**

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

**4. Convert Failures to Benchmark Prompts**

```yaml
id: <category>-<number>  # e.g. mt-001, ada-001
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
- `command_contains` — response or tool outputs contain specific strings
- `non_empty_or_explicit_not_found` — non-empty response or explicit not-found
- `two_step` / `sequence` — multi-step (tool use demonstrates it)

**5. Group Into Benchmark Sets**

Cluster prompts by category. A complete benchmark set should have:
- 4-10 prompts per category
- Varied phrasings (don't make the expected action obvious)
- At least one negative example (task that should NOT use a tool)

### Session Search Tips

1. **Search for the fix, not the failure** — sessions that end with "fixed" often document what broke first
2. **Check session summaries first** — `session_search` returns LLM-generated summaries that surface failures efficiently
3. **Look at truncated sessions** — sessions that were "cut off" mid-investigation often reveal root causes
4. **Cross-reference with logs** — `~/.hermes/logs/errors.log` often has the raw error that sessions later explained

### Output Location

Save mined patterns to `<obsidian-vault>/03-Notes/session-patterns/<YYYY-MM-DD>.md` so they're preserved in long-term memory alongside other session research.

---

## Part 3: Evolutionary Optimization (from hermes-agent-self-evolution)

The full GEPA + DSPy optimization framework from [NousResearch/hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution).

### What Can Be Optimized — The Tier System

| Tier | Target | Risk | Status |
|------|--------|------|--------|
| **Tier 1** | Skill files (SKILL.md) | Low | Highest value, lowest risk |
| **Tier 2** | Tool descriptions | Low-Medium | Medium value, schema must stay frozen |
| **Tier 3** | System prompt sections | High | High value, must stay within 20% size budget |
| **Tier 4** | Tool implementation code | Highest | Darwinian Evolver, strictest guardrails |

**Tier 1 is the primary target for self-improvement** — skills are pure text, easily mutated, directly measurable.

### The Optimization Loop (GEPA Framework)

```
1. SELECT TARGET
   - Pick a skill, prompt section, or tool
   - Load current version as baseline

2. BUILD EVALUATION DATASET
   - Mine SessionDB for real usage examples
   - Or use session-pattern-mining to extract from transcripts
   - Or generate synthetic test cases
   - Split: train / validation / test

3. RUN OPTIMIZER
   - Primary: GEPA (Genetic-Pareto Prompt Evolution)
   - Fallback: DSPy MIPROv2 (Bayesian optimization)
   - Generates mutations, evaluates, selects best

4. EVALUATE & COMPARE
   - Run optimized version on held-out test set
   - Compare: accuracy, cost, latency
   - Statistical significance check

5. DEPLOY (with approval)
   - Git commit the improved version
   - Rollback mechanism via git revert
```

### Evaluation Dataset Sources (in priority order)

**Source A: SessionDB mining (real usage, LLM-as-judge scored)**
- Query SessionDB for sessions where the skill was loaded
- Extract the task the user gave and the agent's full response
- Use LLM-as-judge to score each (task, response) pair on a rubric
- High-scoring pairs → "good" examples; low-scoring → failure cases for GEPA

**Source B: Synthetic generation (bootstrapping)**
- Use a strong model (Claude Opus) to generate 15-30 test cases
- Read the skill file → understand what it does
- Generate (task_input, expected_behavior) pairs
- GEPA works with as few as 3 examples, so start small

**Source C: Hand-curated golden sets**
- Manually written test cases with expected outputs
- Highest quality signal but requires manual effort
- Reserve for critical skills

### LLM-as-Judge Scoring (Multi-Dimensional Rubrics)

For most skills, there's no binary right/wrong — quality is subjective. Use an LLM judge with a rubric:

- Did the agent follow the skill's procedure? (0-1)
- Was the output correct/useful? (0-1)
- Was it concise (within token budget)? (0-1)
- Did it avoid the known failure modes? (0-1)

Aggregate into a composite score.

### Constraint Gates (must pass before any change is valid)

| Constraint | Rule | Why |
|------------|------|-----|
| **Full test suite** | pytest tests/ must pass 100% | Hard floor — nothing ships that breaks existing functionality |
| **Size limits** | Skills ≤15KB, tool descriptions ≤500 chars, system prompts ≤120% of current | Prevents evolutionary bloat |
| **Caching compatibility** | No mid-conversation changes — all changes take effect on new sessions | Preserves prompt caching |
| **Semantic preservation** | Evolved text must not drift from original purpose | Fitness function includes similarity check |
| **Deployment via PR** | All changes go through PR, never direct commit | Human review is mandatory |

### Benchmark Gate Hierarchy

| Benchmark | What It Tests | Speed | Role |
|-----------|---------------|-------|------|
| **TBLite fast subset** | Coding/sysadmin (20 tasks) | ~20 min | Quick regression gate |
| **Full TBLite** | Coding/sysadmin (100 tasks) | ~1-2 hrs | Thorough regression gate |
| **YC-Bench fast_test** | Long-horizon coherence (50 turns) | ~30 min | Coherence check |
| **Session-specific** | Skill-targeted eval dataset | Varies | Primary fitness signal |

**Key principle:** Benchmarks are GATES, not fitness functions. A variant that improves skill quality by 20% but drops TBLite by 5% is REJECTED.

### Practical Considerations

**Cost:**
- GEPA optimization: ~$2-10 per run (API calls only, no GPU)
- Synthetic eval data generation: ~$1-3 per skill
- Start with small eval sets (10-20 examples), scale up for important skills

**Safety:**
- All changes via PR, never direct commit
- Full test suite gate (zero tolerance)
- Character/token budgets enforced
- Caching compatibility checked
- Git-tracked lineage, trivial rollback

**No GPU required** — everything operates via API calls. GEPA mutates text and evaluates via LLM calls, not weight training.

### References

- hermes-agent-self-evolution: https://github.com/NousResearch/hermes-agent-self-evolution
- GEPA paper: ICLR 2026 Oral
- DSPy: https://github.com/stanfordnlp/dspy

---

## Part 4: Tool Description Improvement (Anthropic Pattern)

Anthropic found: "We created a tool-testing agent — when given a flawed MCP tool, it attempts to use the tool and then rewrites the tool description to avoid failures. This process resulted in a 40% decrease in task completion time for future agents using the new description."

This is a separate loop from behavioral benchmarking. Use it when:
- An MCP tool or skill consistently causes failures across multiple agents
- A tool description is vague, misleading, or causes agents to take wrong paths
- You notice agents consistently misusing the same tool

### Tool-Testing Loop

```
IDENTIFY → TEST → DIAGNOSE → PATCH → VERIFY
```

1. **Identify**: Log which tool/skill caused failures in session logs
2. **Test**: Run the tool with various inputs — document failures
3. **Diagnose**: Why does the tool description cause agents to fail?
4. **Patch**: Rewrite the tool description to make failure modes explicit
5. **Verify**: Re-run benchmark tasks using the tool — measure improvement

### Tool Improvement Prompt

```
TASK: Improve the description for [tool/skill name] at [path]

FAILURE OBSERVED:
[what agents did wrong when using this tool]

TOOL DESCRIPTION CURRENTLY:
[copy the current description]

WHY IT FAILS:
[analysis — what in the description caused the wrong behavior]

PROPOSED IMPROVEMENT:
[new description that makes the failure mode explicit]

VERIFICATION:
After patching, run [task type that previously failed] and confirm improvement
```

---

## Critical Rules

- Each lens must RETHINK the question, not just add more information. Technical and contrarian should feel like two researchers who disagree.
- The tension between lenses IS the insight. Don't resolve it away.
- Never present a single-lens finding as a conclusion.
- Separate "what the data shows" from "what I interpret."
- [[open-questions]] is as important as [[executive-summary]].

---

## Folder Structure

```
agentic-self-improvement/
├── SKILL.md                        # This file
├── BENCHMARKS/                     # Behavioral benchmark YAMLs
│   ├── mandatory_tool.yaml
│   ├── act_dont_ask.yaml
│   ├── no_hallucination.yaml
│   ├── verification.yaml
│   ├── prerequisite.yaml
│   ├── path_accuracy.yaml
│   ├── context_grounding.yaml
│   ├── auth_state.yaml
│   └── remember_to_obsidian.yaml
├── REFERENCES/
│   └── guidance_anatomy.md         # Guidance block reference
└── src/                            # Python tooling
    ├── benchmark_runner.py         # Run benchmarks via hermes chat
    ├── failure_analyzer.py         # Analyze results, group failures
    ├── patch_generator.py          # Generate guidance patches
    └── apply_and_verify.py         # Apply patches with auto-revert
```
