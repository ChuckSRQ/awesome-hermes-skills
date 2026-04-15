---
name: agent-evaluation
description: LLM-as-judge evaluation framework for multi-agent outputs. Based on Anthropic's evaluation methodology — score outputs on factual accuracy, completeness, and quality using an LLM judge.
version: 1.0.0
author: Awesome Hermes (based on Anthropic multi-agent research, June 2025)
license: personal
tags: [evaluation, quality, LLM-as-judge, metrics, output-verification]
---

# Agent Evaluation — LLM-as-Judge for Multi-Agent Outputs

Based on Anthropic's evaluation methodology. Key finding: "LLM-as-judge evaluation scales when done well. Research outputs are difficult to evaluate programmatically. LLMs are a natural fit for grading outputs."

## When to Evaluate

Evaluate outputs from Aristotle, Turing, and DaVinci when:
- The task was Complex (Tier 3) and high-stakes
- the user's decision depends on the quality of the output
- You're unsure whether the specialist's output is complete or accurate
- Quality matters more than speed

**Don't evaluate:**
- Simple (Tier 1) outputs — speed over rigor
- Medium (Tier 2) outputs unless quality is in doubt

## Evaluation Rubric (Judge Criteria)

When evaluating with an LLM judge, score each output on these dimensions:

| Dimension | What it measures | Score range |
|-----------|-----------------|-------------|
| **Factual Accuracy** | Do claims match sources? | 0.0–1.0 |
| **Completeness** | Are all requested aspects covered? | 0.0–1.0 |
| **Source Quality** | Did it use primary sources over low-quality secondary? | 0.0–1.0 |
| **Tool Efficiency** | Did it use the right tools a reasonable number of times? | 0.0–1.0 |
| **Verification** | Did it check its own work before finalizing? | 0.0–1.0 |
| **Handoff Quality** | Did it use the structured handoff templates? | 0.0–1.0 |

## Judge Prompt Template

Use this prompt when evaluating a specialist's output:

```
EVALUATION REQUEST

You are an expert judge evaluating an AI agent's output.
Rate the output on factual accuracy, completeness, source quality,
tool efficiency, and verification. Score each dimension 0.0-1.0
with 1.0 being perfect.

OUTPUT TO EVALUATE:
[paste the specialist's output here]

GROUND TRUTH / TASK:
[what the specialist was asked to do]

EVALUATION CRITERIA:
1. Factual Accuracy: Do the claims match verifiable sources?
2. Completeness: Did it cover all requested aspects?
3. Source Quality: Primary sources (>Tier 3 in trust hierarchy)?
4. Tool Efficiency: Appropriate number of tool calls, not too few or too many?
5. Verification: Did the agent check its own work before finalizing?

For each dimension: provide a score (0.0-1.0) and a one-sentence explanation.

FINAL VERDICT: PASS (all scores >= 0.7) / CONDITIONAL PASS (some scores 0.5-0.7) / FAIL (any score < 0.5)

If FAIL or CONDITIONAL PASS: identify the specific weakness and suggest one concrete fix.
```

## Output Score Thresholds

| Score | Interpretation | Action |
|-------|---------------|--------|
| 0.85–1.0 | Excellent | Deliver to the user |
| 0.70–0.84 | Good | Deliver with noted caveats |
| 0.50–0.69 | Marginal | Return to specialist with specific fixes |
| 0.00–0.49 | Poor | Significant rework needed |

## Self-Verification Checklist

Before delivering any specialist output to the user, the lead agent's internal checklist:

```
[ ] Does the output answer the original question?
[ ] Did the specialist use sources? Are sources credible?
[ ] Did the output use the structured handoff format?
[ ] What would change our conclusion? (from the research)
[ ] Is there an open questions section?
[ ] Is there anything the user needs to decide?
[ ] Is this Tier 2 effort delivered at Tier 3 quality?
```

## Evaluation in the Self-Improvement Loop

The agentic-self-improvement skill can incorporate evaluation scores:
- Track which agent types (Aristotle, Turing, DaVinci) have the most failures
- Track which evaluation dimensions score lowest across runs
- Feed this back into prompt improvements for the relevant agent

## Example: Evaluating Aristotle's Research

```
JUDGE OUTPUT:
Factual Accuracy: 0.9 — Claims about multi-agent frameworks match Anthropic blog
Completeness: 0.8 — Covered technical and economic but missed strategic lens
Source Quality: 0.7 — Used Maxim AI blog (Tier 3) and Anthropic primary source
Tool Efficiency: 0.9 — Used 8 web searches, appropriate for scope
Verification: 0.6 — Did not cite specific numbers from Anthropic's data

FINAL VERDICT: CONDITIONAL PASS
REASON: Strategic lens missing from coverage; some claims need primary source backing
FIX: In the next Aristotle brief, explicitly ask for the strategic lens and primary sources
```

## Practical Notes

- For evaluations that DO have a clear right answer (e.g., code that runs or doesn't): use programmatic verification first, then LLM judge for quality dimensions
- Human review catches what automation misses — for high-stakes outputs, always ask "does this feel right to me?"
- Start small: even 5-10 evaluations will reveal patterns
