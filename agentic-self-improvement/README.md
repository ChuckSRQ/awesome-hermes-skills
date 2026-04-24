# 🧪 Agentic Self-Improvement — Closed-Loop Behavioral Benchmarking

> *Closed-loop behavioral benchmarking + evolutionary self-improvement*

**Run behavioral benchmarks against the agent. Detect failures. Generate patches. Apply with auto-revert safety net.**

---

## What It Does

The self-improvement loop turns real conversation failures into automated tests, then evolves skills end-to-end using GEPA (Genetic-Evolutionary Prompt Adjustment) optimization.

**Two modes operate together:**

| Mode | Speed | What it targets |
|------|-------|----------------|
| **Guidance Patch Loop** | Fast, surgical | Specific behavioral failures via guidance blocks |
| **GEPA Optimization** | Principled | Full skill text end-to-end via evolutionary algorithms |

---

## The Core Loop

```
BENCHMARK → DIAGNOSE → PATCH → VERIFY → (auto-revert if regression)
                    ↓
              GEPA OPTIMIZE → EVAL DATASET → EVOLVE → DEPLOY
                    ↓
              SESSION MINE → LLM-AS-JUDGE → NEW BENCHMARKS
```

---

## Benchmarks

| Benchmark | What it tests |
|-----------|---------------|
| `mandatory_tool` | Must use tools for math/hashes/time/files |
| `act_dont_ask` | Act on obvious interpretation, don't ask unnecessary questions |
| `no_hallucination` | Check system state, don't answer from memory/profile |
| `verification` | Verify outputs before finalizing |
| `prerequisite` | Discover before acting |
| `path_accuracy` | Verify paths before using them |
| `context_grounding` | Check actual context, don't assume |
| `auth_state` | Verify credentials before using them |
| `remember_to_obsidian` | Write durable facts to Obsidian, not just memory |

---

## Usage

```bash
# Run all benchmarks, show suggested patches (no changes made)
/self-improve

# Run all benchmarks, auto-apply if improvement, auto-revert if regression
/self-improve --mode=apply

# Run specific category only
/self-improve --benchmarks=mandatory_tool

# Run subset of categories
/self-improve --categories=act_dont_ask,no_hallucination

# View past results
/self-improve --view-results=2026-04-12_1400

# Revert last applied patch
/self-improve --revert
```

---

## How the Guidance Patch Loop Works

**1. Benchmark Runner** — Each prompt runs in isolation. Captures tool calls, tool outputs, final response, and exit code.

**2. Failure Analyzer** — Groups failures by category, computes per-category pass rates.

**3. Patch Generator** — Generates XML guidance blocks for the active model type.

**4. Apply + Verify + Auto-Revert** —
- Run baseline benchmarks → capture pass rates
- Backup current state
- Apply patch
- Re-run benchmarks → compare pass rates
- **If ANY category regresses → auto-revert**
- If all improve → keep patch, report delta

---

## Evolutionary Optimization (GEPA)

GEPA optimizes skill text end-to-end using genetic algorithms:

1. **Select target** — Pick a skill or prompt section
2. **Build evaluation dataset** — Mine real usage examples from SessionDB or generate synthetic cases
3. **Run optimizer** — GEPA generates mutations, evaluates, selects the best
4. **Evaluate & compare** — Run on held-out test set
5. **Deploy via PR** — Git commit with human review required

**Constraint gates (must pass before any change is valid):**
- Full test suite must pass 100%
- Skills ≤15KB, tool descriptions ≤500 chars
- No mid-conversation changes
- All changes via PR with human review

---

## Safety

- **Always backs up** before applying any patch
- **Auto-revert** if any category regresses after patch
- **Suggest first** is the default mode — nothing is modified without explicit `--mode=apply`
- All changes via PR with human review
- No mid-conversation hot-swaps

---

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — production-ready AI agent skills.*
