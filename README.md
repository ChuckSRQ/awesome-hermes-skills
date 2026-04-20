# 🧩 Awesome Hermes Skills — Core Four

<p align="center">
  <img src="https://img.shields.io/badge/Hermes-Agent-v2.0-6366f1?style=for-the-badge" alt="Hermes Agent v2.0" />
  <img src="https://img.shields.io/badge/Skills-4-8B5CF6?style=for-the-badge" alt="4 Skills" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="MIT License" />
</p>

Four production-ready skills for Hermes Agent — no fluff, no extras. Each one earns its place.

---

## 🪽 Artifact Preview · `artifact-preview/`

> *Write code. See it live. Instantly. Never lose a version. 🔥*

**The "Claude Artifacts" experience — for any AI agent.**

Write a prompt → get a polished, interactive HTML artifact → Chrome opens automatically with live reload. Portrait, horizontal, or full-screen modes. Auto-detects the right layout from your HTML. Inline editor. Retina screenshots. Zero config.

| Feature | What it does |
|---------|-------------|
| ⚡ **Live Reload** | SSE pushes updates the instant you save — no refresh buttons |
| 🧠 **Auto-Detect** | Reads meta tags or content heuristics, picks portrait/horizontal/full automatically |
| 📐 **Content-Shaped** | Portrait (~430×844) for phone apps, horizontal (~1240×720) for dashboards, full for websites |
| ✏️ **Inline Editor** | Code / Split / Preview tabs with `Cmd+Shift+E` toggle |
| 📸 **Screenshots** | One-click Retina capture to macOS Preview |
| 💾 **Persistent History** | Every save archived — retrieve any previous version instantly |
| 🆕 **Save as New** | Fork current artifact without overwriting — new entry in history |

**One-line install:**
```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash
```

**Uninstall (also one-line):**
```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/uninstall.sh | bash
```

---

## 🔬 Deep Research · `deep-research/`

> *9 lenses. One question. Analysis that single Google searches can't touch.*

**A structured multi-angle research engine.** Forces you to think about any question from 9 fundamentally different angles — each lens surfaces things the others miss.

| Lens | What it asks |
|------|-------------|
| 🔧 Technical | Mechanics, data, hard numbers — strip the narrative |
| 💰 Economic | Money flows, incentives, cost structures, who pays/profits |
| 📜 Historical | Patterns, precedent, what failed before |
| 🏢 Business | Competitive landscape, unit economics, who's winning/losing |
| ♟️ Strategic | Key moves, leverage points, game theory — 3–10 year view |
| 👤 Customer | Real buyer vs. user, JTBD, trust signals, purchase blockers |
| 📦 Product | Capabilities, limits, failure modes, MVPs |
| 🤨 Contrarian | Stress-test consensus — who benefits from the current narrative? |
| 🧱 First-Principles | Rebuild from ground truth — forget all assumptions |

**Output:** executive summary · deep-dive · key players · open questions

**Perfect for:** investment research, competitive analysis, architecture decisions, market sizing, due diligence, understanding emerging tech

**Invocation:** `do deep research on [your question]`

**Knowledge base:** `~/research-skill-graph/`

---

## 🧪 Agentic Benchmark Testing · `agentic-self-improvement/`

> *Closed-loop behavioral benchmarking + evolutionary self-improvement*

**Run behavioral benchmarks against the agent. Detect failures. Generate patches. Apply with auto-revert safety net.**

Implements the full GEPA (Genetic-Evolutionary Prompt Adjustment) optimization loop with DSPy integration. Turns real conversation failures into automated tests, then evolves skills end-to-end.

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

**Usage:**
```bash
/self-improve                              # run all benchmarks, show patches
/self-improve --mode=apply                 # apply + auto-revert if regression
/self-improve --benchmarks=mandatory_tool  # specific benchmark
/self-improve --revert                     # revert last patch
```

---

## ⚡ GH Copilot · `gh-copilot/`

> *GitHub Copilot CLI plugin — 23 Hermes development skills.*

**A plugin for `gh copilot` CLI that wires 23 production skills directly into GitHub Copilot.**

Invoke any skill via `/skill` or `gh copilot -- -i "use <skill>"`.

| Category | Skills |
|----------|--------|
| **Code Workflow** | code-review · test-driven-development · systematic-debugging · plan · subagent-driven-development |
| **AI Agents** | claude-code · codex · opencode · subagent-delegation |
| **GitHub** | github-pr-workflow · github-code-review · github-repo-management · github-issues · codebase-inspection |
| **Debugging** | triage-issue · invisible-elements-debugging |
| **Diagrams** | architecture-diagram · excalidraw |
| **MLOps** | vllm · llama-cpp · gguf |
| **MCP** | mcporter · native-mcp |

### GH PR Workflow (key rules)

| Rule | Detail |
|------|--------|
| **Branch → PR → Squash/Merge** | Feature branches use `feat/`, `fix/`, `refactor/`, `docs/`, `ci/` naming |
| **Carlos merges** | Agent never merges — PR submitted for Carlos's review and merge |
| **Conventional Commits** | `type(scope): short description` — feat, fix, refactor, docs, test, ci, chore, perf |
| **CI auto-fix loop** | Detect failure → read logs → patch → push → re-check → repeat (max 3 attempts, then ask) |

```bash
gh copilot -- -i "use github-pr-workflow to open a PR for this fix" --allow-all
gh copilot -- -i "use code-review to review the current branch" --allow-all
```

---

## 📁 Repo Structure

```
awesome-hermes-skills/
├── artifact-preview/           # Live HTML preview server + Chrome launcher
├── deep-research/              # 9-lens research engine
├── agentic-self-improvement/   # Behavioral benchmarking + GEPA optimization
├── gh-copilot/                # GitHub Copilot CLI plugin (23 skills)
├── README.md                   # This file
├── LICENSE                     # MIT
└── agents.md                   # Repo operating rules
```

---

## ⚙️ Setup

```bash
# Clone
git clone https://github.com/ChuckSRQ/awesome-hermes-skills.git ~/.hermes/skills

# Individual skills
cp -r awesome-hermes-skills/artifact-preview ~/.hermes/skills/
cp -r awesome-hermes-skills/deep-research ~/.hermes/skills/
cp -r awesome-hermes-skills/agentic-self-improvement ~/.hermes/skills/
cp -r awesome-hermes-skills/gh-copilot ~/.hermes/skills/
```

---

## 📜 License

MIT — use freely, modify freely, credit this repo if you're feeling generous.

<p align="center">
  <sub>Maintained with ❤️ for the Hermes Agent community</sub><br/>
  <a href="https://github.com/ChuckSRQ/awesome-hermes-skills">GitHub</a> ·
  <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a>
</p>
