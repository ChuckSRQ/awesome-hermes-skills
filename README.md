# Awesome Hermes Skills

<p align="center">
  <img src="https://img.shields.io/badge/Hermes-Agent-v2.0-6366f1?style=for-the-badge" alt="Hermes Agent v2.0" />
  <img src="https://img.shields.io/badge/Skills-4%20Featured-f59e0b?style=for-the-badge" alt="4 Featured Skills" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="MIT License" />
</p>

<p align="center">
  A curated collection of production-ready skills for <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a>.<br/>
  Only the ones worth keeping.
</p>

---

## Featured Skills

### 🪽 [Artifact Preview](productivity/artifact-preview/SKILL.md)
> *Write code. See it live. Instantly. Auto-detects the right window size from your HTML.*

Write a prompt. Get a **real, working app** — not a skeleton, not a toy. A polished, interactive artifact that opens live in a Chrome window the moment it's generated. Three content-shaped modes. Auto-detection. Live reload. Inline editor. Retina screenshots. All in seconds.

**Perfect for:** dashboards, UI components, prototypes, interactive demos, forms, games, data visualizations, landing pages, charts, plugins

```
make a dashboard showing my team stats
build a landing page with a contact form
show me an interactive map component
create a tic-tac-toe game
```

**What you get:**
- 🧠 **Auto-detect mode** — reads your HTML meta tags or content heuristics, picks portrait/horizontal/full automatically
- 🖥️ **Three content-shaped windows** — portrait (~430×844) for phone apps, horizontal (~1240×720) for dashboards, full for websites
- ⚡ **Zero-latency live reload** — SSE pushes updates the instant you save, no refresh buttons
- 📐 **Smart card** — hugs small widgets, expands edge-to-edge for full-width websites
- ✏️ **Inline HTML editor** — Code / Split / Preview tabs with `Cmd+Shift+E` toggle
- 📸 **Retina screenshots** — one-click capture to macOS Preview with system share sheet
- 🎨 **Design system** — Instrument Sans, violet accent (#8B5CF6), modern CSS
- 🔌 **Zero deps** — one HTML file, no npm, no build step
- 🍎 **macOS native** — AppleScript window management, `NSScreen` API, Chrome integration

**[→ Read the full skill documentation](productivity/artifact-preview/SKILL.md)**

---

### 🔬 [Deep Research](deep-research/SKILL.md)
> *9 lenses. One question. Analysis that single Google searches can't touch.*

A structured multi-angle research engine that forces you to think about any question from 9 fundamentally different angles — technical, economic, historical, business, strategic, customer, product, contrarian, and first-principles. Each lens surfaces things the others miss.

**Perfect for:** investment research, competitive analysis, architecture decisions, market sizing, due diligence, understanding emerging tech

```
do deep research on whether Solana can challenge Ethereum
deep research on the AI coding agent landscape
research: should we build a mobile app or web app first
```

**What you get:**
- 9-lens structured analysis
- 5-tier source trust scoring
- Executive summary + deep-dive + key players + open questions
- Contradiction tracking between lenses
- Compound knowledge that builds over time

**[→ Read the full skill documentation](deep-research/SKILL.md)**

---

### 🧪 [Agentic Self-Improvement](agentic-self-improvement/SKILL.md)
> *Closed-loop behavioral benchmarking + evolutionary self-improvement*

Run behavioral benchmarks against the agent, detect failure patterns, generate guidance patches, and apply them with an auto-revert safety net. Implements the full GEPA (Genetic-Evolutionary Prompt Adjustment) optimization loop with DSPy integration.

**Perfect for:** improving agent reliability, catching regressions, turning real failures into automated tests, evolving skills end-to-end

```
# Run all behavioral benchmarks
/self-improve

# Run + auto-apply patches if improvement detected
/self-improve --mode=apply

# Run specific benchmark category
/self-improve --benchmarks=mandatory_tool.yaml
```

**Benchmark categories covered:**
- `mandatory_tool` — must use tools for math/hashes/time/files
- `act_dont_ask` — act on obvious interpretation, don't ask for clarification unnecessarily
- `no_hallucination` — check system state, don't answer from memory
- `verification` — verify outputs before finalizing
- `prerequisite` — discover before acting
- `path_accuracy` — verify paths before using them
- `context_grounding` — check actual context, don't assume
- `auth_state` — verify credentials before using them
- `remember_to_obsidian` — write durable facts to Obsidian, not just memory

**[→ Read the full skill documentation](agentic-self-improvement/SKILL.md)**

---

### ⚡ [Copilot](copilot/README.md)
> *Give your AI a real workbench — terminal, browser, and files, all accessible.*

An enhanced GitHub Copilot CLI plugin for Hermes Agent that gives the AI a real coding workbench: terminal access, browser automation, file system navigation, and multi-agent task decomposition. Built on OpenCode with deep tool access and safety guardrails.

**Perfect for:** complex build tasks, browser automation, multi-step coding workflows, delegated coding to subagents

```
build a complete React app from scratch
run the tests and fix any failures
crawl this website and extract the pricing data
```

**What you get:**
- Full terminal access with sandboxed subprocess execution
- Browser automation via Playwright (click, type, navigate, screenshot)
- File system operations with safe path boundaries
- Multi-agent delegation with result synthesis
- Safety guardrails to block dangerous commands

**[→ Read the full skill documentation](copilot/README.md)**

---

## 🚀 Quick Start

```bash
# Clone the collection
git clone https://github.com/ChuckSRQ/awesome-hermes-skills.git ~/.hermes/skills/awesome-hermes-skills

# Individual skills (copy into your skills directory)
cp -r ~/.hermes/skills/awesome-hermes-skills/productivity/artifact-preview ~/.hermes/skills/
cp -r ~/.hermes/skills/awesome-hermes-skills/deep-research ~/.hermes/skills/
cp -r ~/.hermes/skills/awesome-hermes-skills/agentic-self-improvement ~/.hermes/skills/
cp -r ~/.hermes/skills/awesome-hermes-skills/copilot ~/.hermes/skills/
```

Skills auto-load when you ask for them. Say `"make me a dashboard"` and Artifact Preview opens. Say `"do deep research on X"` and Deep Research activates.

---

## 📜 License

MIT — use freely, modify freely, credit Awesome Hermes if you're feeling generous.

---

<p align="center">
  <sub>Maintained with ❤️ for the Hermes Agent community</sub><br/>
  <a href="https://github.com/ChuckSRQ/awesome-hermes-skills">GitHub</a> ·
  <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a> ·
  <a href="https://github.com/NousResearch/hermes-agent-self-evolution">HERMES Self-Evolution</a>
</p>
