# 🔬 Deep Research — 9 Lenses, One Question

> *9 lenses. One question. Analysis that single Google searches can't touch.*

**A structured multi-angle research engine.** Forces you to think about any question from 9 fundamentally different angles — each lens surfaces things the others miss.

**Knowledge base:** `~/research-skill-graph/`

---

## The 9 Lenses

| Lens | What it asks |
|------|-------------|
| 🔧 **Technical** | Mechanics, data, hard numbers — strip the narrative |
| 💰 **Economic** | Money flows, incentives, cost structures, who pays/profits |
| 📜 **Historical** | Patterns, precedent, what failed before |
| 🏢 **Business** | Competitive landscape, unit economics, who's winning/losing |
| ♟️ **Strategic** | Key moves, leverage points, game theory — 3–10 year view |
| 👤 **Customer** | Real buyer vs. user, JTBD, trust signals, purchase blockers |
| 📦 **Product** | Capabilities, limits, failure modes, MVPs |
| 🤨 **Contrarian** | Stress-test consensus — who benefits from the current narrative? |
| 🧱 **First-Principles** | Rebuild from ground truth — forget all assumptions |

---

## What You Get

Every deep research run produces 4 documents inside `~/research-skill-graph/projects/[project-name]/`:

- **executive-summary.md** — 500 words max. What did we learn? What does it mean? What's unknown?
- **deep-dive.md** — Full analysis organized by lens, cross-references and contradictions highlighted
- **key-players.md** — People, organizations, countries that matter most
- **open-questions.md** — What we STILL don't know. Often more valuable than findings.

---

## How to Run

```
do deep research on [your question]
```

Or load the skill explicitly, then ask your question. The agent will run all 9 lenses live so you can see the reasoning and course-correct mid-flight.

---

## The Compound Effect

This system gets better over time:
- `knowledge/concepts.md` and `knowledge/data-points.md` accumulate across ALL projects
- After 5 projects, the AI starts with 200+ verified data points and 50+ defined concepts
- Every `open-questions.md` from one project becomes seeds for the next

---

## Perfect For

- Investment research
- Competitive analysis
- Architecture decisions
- Market sizing
- Due diligence
- Understanding emerging tech

---

## How It Works

**Step 1:** Read the command center at `~/research-skill-graph/index.md`

**Step 2:** Pick the right framework for your question type:
- "Is X true?" → Verification framework
- "Why is X happening?" → Causal analysis framework
- "What happens if X?" → Scenario planning framework
- "What should I do about X?" → Decision support framework

**Step 3:** Apply the 5-tier trust system to every source:
- Tier 1: Primary data (raw datasets, peer-reviewed studies)
- Tier 2: Expert analysis (research institutions, long-form journalism)
- Tier 3: Informed commentary (expert blogs, think tank reports)
- Tier 4: General media (major news, Wikipedia — verify upstream)
- Tier 5: Social/anecdotal (Twitter, Reddit — signal detection only)

**Step 4:** Run all 9 lenses — each one must *rethink* the question, not just add more information.

**Step 5:** Resolve or document contradictions between lenses. Tension IS the insight.

---

## ⚠️ Critical Rules

- Each lens must RETHINK the question, not just add more information. Technical and contrarian should feel like two researchers who disagree.
- Never present a single-lens finding as a conclusion.
- Separate "what the data shows" from "what I interpret."
- `[[open-questions]]` is as important as `[[executive-summary]]`.

---

## 🔥 Live Research Is Non-Negotiable

When you say "do deep research," you want to SEE the agent working — live searches, visible reasoning, real-time synthesis. Show the moves, the choices, the findings. This is how trust is built. The user can course-correct mid-stream when they can see the thinking.

Background subagent delegation has proven unreliable for research — subagents can get interrupted before completing. Only use background agents after getting explicit buy-in from the user.

---

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — production-ready AI agent skills.*
