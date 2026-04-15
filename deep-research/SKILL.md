---
name: deep-research
description: Multi-lens research engine — one question, 9 angles, synthesized analysis. Uses ~/research-skill-graph/ as the knowledge base. Load this skill when given a research question and use it to produce deep, structured analysis. Invoke by saying "do deep research on [question]".
keywords: [deep-research, deep research, analysis, multi-lens, research, synthesis, strategy]
version: 1.2.0
author: Hermes Community
license: mit
related_skills:
  - last30days  # Tier 5 social sentiment — Reddit + X via last30days covers the social/anecdotal layer referenced in the 5-tier trust system (source-evaluation.md). Load this for customer, contrarian, and business lenses.
---

# Deep Research

A local research engine that takes ONE question and produces multi-angle analysis no single Google search or prompt could match.

**Knowledge base:** `~/research-skill-graph/`
**Invocations:** say "do deep research on [your question]" or "/skill deep-research" then ask your question

---

## How It Works

The system forces structured thinking through 9 research lenses, each rethinking the question from a fundamentally different angle. Lenses are defined in the skill graph folder and evolve over time.

**The 9 Lenses (in execution order):**
1. **technical** — mechanics, data, hard numbers. Strip away narrative.
2. **economic** — money flows, incentives, cost structures, who pays/profits.
3. **historical** — patterns, precedent, what failed before.
4. **business** — competitive landscape, unit economics, who's winning/losing.
5. **strategic** — key moves, leverage points, game theory. What matters in 3-10 years.
6. **customer** — real buyer vs. user, JTBD, trust signals, purchase blockers.
7. **product** — capabilities, limits, failure modes, MVPs.
8. **contrarian** — stress-test the consensus. Who benefits from the current narrative?
9. **first-principles** — rebuild from ground truth. Forget assumptions.

---

## Execution Protocol
## Execution Protocol
When you receive a research question:

**Step 1:** Read the command center at `~/research-skill-graph/index.md` — it contains the full briefing template and node map.

**Step 2:** Read `methodology/research-frameworks.md` to pick the right approach for the question type:
- "Is X true?" → Verification framework
- "Why is X happening?" → Causal analysis framework
- "What happens if X?" → Scenario planning framework
- "What should I do about X?" → Decision support framework

**Step 3:** Read `methodology/source-evaluation.md` — apply the 5-tier trust system to every source:
- Tier 1: Primary data (raw datasets, peer-reviewed studies)
- Tier 2: Expert analysis (research institutions, long-form journalism)
- Tier 3: Informed commentary (expert blogs, think tank reports)
- Tier 4: General media (major news, Wikipedia — verify upstream)
- Tier 5: Social/anecdotal (Twitter, Reddit — signal detection only)

**Step 4:** Run ALL 9 lenses. For each lens:
a. Read the lens file
b. Research the topic THROUGH that lens only
c. Record findings, sources, and confidence level
d. Note contradictions with previous lenses

**Step 5:** Read `methodology/contradiction-protocol.md` — resolve or document disagreements between lenses. Contradictions are features, not bugs.

**Step 6:** Read `methodology/synthesis-rules.md` — combine findings across lenses without flattening nuance.

**Step 7:** Produce all 4 output files inside `projects/[project-name]/`:
- **executive-summary.md** — 500 words max. What did we learn? What does it mean? What's unknown?
- **deep-dive.md** — Full analysis organized by lens, cross-references and contradictions highlighted.
- **key-players.md** — People, organizations, countries that matter most.
- **open-questions.md** — What we STILL don't know. Often more valuable than findings.

**Step 8:** Update `knowledge/concepts.md` and `knowledge/data-points.md` with everything learned.

## Execution Mode (Critical)

**DO: Live visible research for the user.**
When the user says "do deep research," they want to SEE you working — live searches, visible reasoning, real-time synthesis. Show the moves, the choices, the findings. This is how trust is built. The user can course-correct mid-stream when they can see your thinking.

**DON'T: Background delegation for Deep Research.**
Background subagent delegation via `delegate_task` has proven unreliable on some model setups — subagents can get interrupted before completing. Only use background agents after getting explicit buy-in from the user.

**Exception:** For IMPLEMENTATION after research is done (building skills, writing files), background delegation is fine — that's mechanical work, not reasoning work.

**Mid-Research Course Correction (Important Pattern):**
Occasionally a single search result or source fundamentally changes the research thesis mid-flight. Example: researching "AI agent reputation protocols" → discovers ERC-8004 already deployed Jan 2026 with identical core concept. The thesis shifts from "should you build this?" to "pivot to analytics layer on top of ERC-8004." When this happens:
1. Note the discovery explicitly ("Finding X changes the premise")
2. Adjust the remaining lenses to test the new hypothesis, not the original
3. Update the executive summary to reflect what changed and why
4. Document the shift in the deep-dive under the lens that triggered it
This is a FEATURE of live research, not a failure. The structured lens system handles the course correction gracefully.

**Payments in Crypto/Web3 Projects (Critical Rule):**
When producing a spec for any crypto or web3 product, do NOT default to Stripe, credit cards, email auth, or any fiat infrastructure — even if it seems like the obvious solution. Crypto products require crypto-native payments. Default to:
- **x402 (HTTP 402)** for API payments: wallet signature, no account, no KYC, per-request billing
- **No accounts required** for read access; anonymity is a first principle, not a feature
- **No Google Analytics** — use Plausible Analytics or a self-hosted alternative
- **No fiat on-ramps** in the spec unless explicitly requested

If Stripe or any fiat payment appears in a draft spec and the project is blockchain/crypto/web3 adjacent, it will be rejected. Confirm the payment model BEFORE including it in a spec.

---

## Critical Rules

- Each lens must RETHINK the question, not just add more information. Technical and contrarian should feel like two researchers who disagree.
- The tension between lenses IS the insight. Don't resolve it away.
- Never present a single-lens finding as a conclusion.
- Separate "what the data shows" from "what I interpret."
- [[open-questions]] is as important as [[executive-summary]].

---

## Folder Structure (lived in ~/research-skill-graph/)

```
research-skill-graph/
├── index.md                      # Command center (start here)
├── research-log.md               # All past projects with key findings
├── methodology/
│   ├── research-frameworks.md    # How to pick the right approach
│   ├── source-evaluation.md       # 5-tier trust system
│   ├── synthesis-rules.md        # How to combine findings
│   └── contradiction-protocol.md # How to handle disagreements
├── lenses/                       # The 9 research lenses
│   ├── technical.md
│   ├── economic.md
│   ├── historical.md
│   ├── business.md
│   ├── strategic.md
│   ├── customer.md
│   ├── product.md
│   ├── contrarian.md
│   └── first-principles.md
├── projects/                     # One subfolder per research project
│   └── [project-name]/
│       ├── executive-summary.md
│       ├── deep-dive.md
│       ├── key-players.md
│       └── open-questions.md
├── sources/
│   └── source-template.md        # Copy for each major source
└── knowledge/
    ├── concepts.md               # Accumulates across ALL projects
    └── data-points.md            # Verified numbers, always with attribution
```

---

## The Compound Effect

This system gets better over time:
- `knowledge/concepts.md` and `knowledge/data-points.md` accumulate across ALL projects
- After 5 projects, the AI starts with 200+ verified data points and 50+ defined concepts
- `research-log.md` tracks every project — the 10th project starts from everything already learned
- [[open-questions]] from one research become seeds for the next

---

## When to Use Each Depth Level

**Level 1 (30 min):** 3 lenses max, top 5 sources. Directional understanding.
**Level 2 (2-3 hrs):** All 9 lenses, 15-25 sources. Informed opinion backed by evidence.
**Level 3 (1-2 days):** All 9 lenses with sub-questions, 50+ sources including primary data. Publishable analysis.
