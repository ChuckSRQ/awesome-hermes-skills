# Awesome Hermes Skills

<p align="center">
  <img src="https://img.shields.io/badge/Hermes-Agent-v2.0-6366f1?style=for-the-badge" alt="Hermes Agent v2.0" />
  <img src="https://img.shields.io/badge/Skills-83+-f59e0b?style=for-the-badge" alt="83+ Skills" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/badge/Category-Productivity-06b6d4?style=for-the-badge" alt="Productivity" />
</p>

<p align="center">
  A curated, production-ready collection of skills for <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a>.<br/>
  Drop them in and use them immediately — no setup required (most of them).
</p>

---

## ⭐ Featured Skills

These are the crown jewels — the skills that get used daily and make Hermes genuinely powerful.

### 🪽 [Artifact Preview v3.0](skills/productivity/artifact-preview/README.md) <img src="https://img.shields.io/badge/NEW-v3.0-8B5CF6?style=flat-square" alt="v3.0" />

> *Write code. See it live. Instantly. Auto-detects the right window size from your HTML.*

Write a prompt. Get a **real, working app** — not a skeleton, not a toy. A polished, interactive artifact that opens live in a Chrome window the moment it's generated. Three content-shaped modes. Auto-detection. Live reload. Inline editor. Retina screenshots. All in seconds.

**Perfect for:** dashboards, UI components, prototypes, interactive demos, forms, games, data visualizations, landing pages, charts, plugins

```
make a dashboard showing my team stats
build a landing page with a contact form
show me an interactive map component
create a tic-tac-toe game
```

#### 📥 Install

```bash
mkdir -p ~/artifact-preview
cp skills/productivity/artifact-preview/open-chrome.sh ~/artifact-preview/
cp skills/productivity/artifact-preview/open-chrome.applescript ~/artifact-preview/
cp skills/productivity/artifact-preview/server.py ~/artifact-preview/
cp skills/productivity/artifact-preview/index.html ~/artifact-preview/
chmod +x ~/artifact-preview/open-chrome.sh
cd ~/artifact-preview && python3 server.py &
```

#### 🆕 What's new in v3.0

| Feature | v2.0 | v3.0 |
|---------|------|------|
| Window modes | 2 (square + full tab) | **3 — portrait, horizontal, full** |
| Mode selection | Manual | **Auto-detect from HTML** |
| Full screen | New tab | **New window, fills primary display** |
| Multi-monitor | Spans all screens | **Main display only** |
| Chrome launch | Profile picker + blank tabs | **Clean, no dialog** |
| Preview card | Always 960px max | **Hugs small, fills for websites** |

#### 🎯 Core features

- 🧠 **Auto-detect mode** — reads your HTML meta tags or content heuristics, picks portrait/horizontal/full automatically
- 🖥️ **Three content-shaped windows** — portrait (~430×844) for phone apps, horizontal (~1240×720) for dashboards, full for websites
- ⚡ **Zero-latency live reload** — SSE pushes updates the instant you save, no refresh buttons
- 📐 **Smart card** — hugs small widgets, expands edge-to-edge for full-width websites
- ✏️ **Inline HTML editor** — Code / Split / Preview tabs with `Cmd+Shift+E` toggle
- 📸 **Retina screenshots** — one-click capture to macOS Preview with system share sheet
- 🎨 **Design system** — Instrument Sans, violet accent (#8B5CF6), modern CSS
- 🔌 **Zero deps** — one HTML file, no npm, no build step
- 🍎 **macOS native** — AppleScript window management, `NSScreen` API, Chrome integration

**[→ Read the full skill documentation](skills/productivity/artifact-preview/README.md)**

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

---

### 🧪 [Agentic Benchmark Testing](skills/agentic-self-improvement)

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

---

## 🚀 Quick Start

```bash
# Clone the entire collection
git clone https://github.com/ChuckSRQ/awesome-hermes-skills.git ~/.hermes/skills

# Or copy individual skill directories
cp -r ~/.hermes/skills/awesome-hermes-skills/deep-research ~/.hermes/skills/
cp -r ~/.hermes/skills/awesome-hermes-skills/productivity/artifact-preview ~/.hermes/skills/
```

Skills auto-load when you ask for them. Say `"do deep research on X"` or `"make me a dashboard"` and Hermes will load the right skill automatically.

---

## 📂 Browse by Category

### 🧠 AI & Coding Agents
| Skill | Description |
|-------|-------------|
| [Claude Code](skills/autonomous-ai-agents/claude-code) | Delegate to Anthropic's Claude Code CLI |
| [Codex](skills/autonomous-ai-agents/codex) | Delegate to OpenAI Codex |
| [OpenCode](skills/autonomous-ai-agents/opencode) | Delegate to OpenSource Code agent |
| [Subagent Delegation](skills/autonomous-ai-agents/subagent-delegation) | Rules for delegating to subagents safely |
| [Requesting Code Review](skills/software-development/requesting-code-review) | Pre-commit verification pipeline |

### 🍎 Apple Ecosystem
| Skill | Description |
|-------|-------------|
| [iMessage](skills/apple/imessage) | Send/receive SMS and iMessages |
| [Reminders](skills/apple/apple-reminders) | Manage Apple Reminders lists |
| [Find My](skills/apple/findmy) | Track devices and AirTags |
| [Apple Notes](skills/apple/apple-notes) | Read/write Apple Notes |

### 💡 Brainstorming & Design
| Skill | Description |
|-------|-------------|
| [Brainstorming](skills/brainstorming) | Socratic pre-implementation refinement |
| [Write a PRD](skills/write-a-prd) | Turn a conversation into a structured spec |
| [PRD to Plan](skills/prd-to-plan) | Convert a PRD into implementation phases |
| [PRD to Issues](skills/prd-to-issues) | Break a PRD into grabbable GitHub issues |
| [Grill Me](skills/grill-me) | Relentless Socratic questioning of a plan |
| [Ubiquitous Language](skills/ubiquitous-language) | DDD-style glossary extraction |

### 🧪 Code Quality
| Skill | Description |
|-------|-------------|
| [Test-Driven Development](skills/software-development/test-driven-development) | RED-GREEN-REFACTOR cycle with anti-patterns |
| [Systematic Debugging](skills/software-development/systematic-debugging) | Root-cause tracing framework |
| [Code Review](skills/software-development/code-review) | Security-focused review checklist |
| [Triage Issue](skills/triage-issue) | Explore a codebase to find the bug |

### 📄 Documents & Media
| Skill | Description |
|-------|-------------|
| [PDF](skills/pdf) | Extract, merge, split, watermark PDFs |
| [DOCX](skills/docx) | Create and edit Word documents |
| [PPTX](skills/pptx) | Create PowerPoint presentations |
| [XLSX](skills/xlsx) | Build Excel workbooks with formulas |
| [OCR & Documents](skills/productivity/ocr-and-documents) | Extract text from scans and PDFs |
| [YouTube Content](skills/media/youtube-content) | Fetch transcripts and transform content |

### 🎨 Creative
| Skill | Description |
|-------|-------------|
| [ASCII Art](skills/creative/ascii-art) | 571-font ASCII art generation |
| [ASCII Video](skills/creative/ascii-video) | Full ASCII video pipeline |
| [Architecture Diagrams](skills/creative/architecture-diagram) | Dark-themed system diagrams |
| [Excalidraw](skills/creative/excalidraw) | Hand-drawn style diagrams |
| [p5.js](skills/creative/p5js) | Interactive generative art |
| [Manim Video](skills/creative/manim-video) | Math/animation videos |
| [Songwriting + AI Music](skills/creative/songwriting-and-ai-music) | Lyrics and Suno prompts |

### 🤖 MLOps & AI
| Skill | Description |
|-------|-------------|
| [Axolotl](skills/mlops/training/axolotl) | Fine-tune LLMs with Axolotl |
| [Unsloth](skills/mlops/training/unsloth) | 2-5x faster fine-tuning |
| [vLLM](skills/mlops/inference/vllm) | High-throughput model serving |
| [llama.cpp](skills/mlops/inference/llama-cpp) | CPU/Apple Silicon inference |
| [GGUF Quantization](skills/mlops/inference/gguf) | Efficient model quantization |
| [DSPy](skills/mlops/research/dspy) | Declarative AI system programming |
| [Weights & Biases](skills/mlops/evaluation/weights-and-biases) | Experiment tracking |
| [Whisper](skills/mlops/models/whisper) | Speech recognition |
| [Stable Diffusion](skills/mlops/models/stable-diffusion) | Text-to-image generation |

### 📊 Research
| Skill | Description |
|-------|-------------|
| [arXiv](skills/research/arxiv) | Academic paper search and retrieval |
| [Polymarket](skills/research/polymarket) | Prediction market data |
| [Blog Watcher](skills/research/blogwatcher) | RSS/Atom feed monitoring |
| [Last30days](skills/research/last30days) | Social search across Reddit + X |
| [LLM Wiki](skills/research/llm-wiki) | Karpathy's LLM knowledge base |

### 💳 Payments & Web3
| Skill | Description |
|-------|-------------|
| [Stripe Integration](skills/stripe-integration) | Payment flows, webhooks, PCI compliance |
| [x402 Payments](skills/public-apis) | Crypto-native HTTP 402 payments |

### 🏠 Smart Home & Leisure
| Skill | Description |
|-------|-------------|
| [Philips Hue](skills/smart-home/openhue) | Control Hue lights, rooms, scenes |
| [Find Nearby](skills/leisure/find-nearby) | Restaurants, cafes, bars, pharmacies |
| [Minecraft Server](skills/gaming/minecraft-modpack-server) | Modded server setup |
| [Pokemon Player](skills/gaming/pokemon-player) | Autonomous Pokemon play |

### 🔧 Productivity & Ops
| Skill | Description |
|-------|-------------|
| [Linear](skills/productivity/linear) | Manage Linear issues via API |
| [Notion](skills/productivity/notion) | Notion pages and databases |
| [Google Workspace](skills/productivity/google-workspace) | Gmail, Calendar, Drive, Sheets |
| [Obsidian](skills/note-taking/obsidian) | Read/write/search vault notes |
| [Himalaya Email](skills/email/himalaya) | CLI email via IMAP/SMTP |
| [GitHub PR Workflow](skills/github/github-pr-workflow) | Full PR lifecycle |
| [Webhook Subscriptions](skills/devops/webhook-subscriptions) | Event-driven webhook management |
| [Pre-commit Hooks](skills/setup-pre-commit) | Husky + lint-staged setup |

### 🌐 Web Development
| Skill | Description |
|-------|-------------|
| [Web Asset Generator](skills/web-asset-generator) | Favicons, app icons, PWA icons |
| [Typography](skills/typography) | Font selection and pairing |
| [Color & Palette](skills/color-and-palette) | Color theory and palette building |
| [Aesthetic Principles](skills/aesthetic-principles) | Core web design principles |
| [TALL Stack Dev](skills/tall-stack-dev) | Laravel + Tailwind + Alpine + Livewire |

---

## 🤝 Contributing

Found a skill worth sharing? The bar is simple: **does this solve a real problem in a way that saves time?**

- Open an issue to discuss before submitting
- PRs welcome — keep it clean and MIT-licensed
- Personal info is scrubbed before merging (see repo for scrubbing guide)

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
