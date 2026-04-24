# ⚡ GH Copilot — GitHub Copilot CLI Plugin

> *23 Hermes development skills, wired into GitHub Copilot.*

**A plugin for `gh copilot` CLI that wires 23 production skills directly into GitHub Copilot.**

Invoke any skill via `/skill` or `gh copilot -- -i "use <skill>"`.

---

## What It Does

GH Copilot bridges the gap between GitHub Copilot CLI and the full Hermes skills library. When you install this plugin, GitHub Copilot gains access to 23 specialized skills covering code workflows, AI agents, GitHub operations, debugging, diagrams, and MLOps.

---

## 23 Skills Across 7 Categories

| Category | Skills |
|----------|--------|
| **Code Workflow** | code-review · test-driven-development · systematic-debugging · plan · subagent-driven-development |
| **AI Agents** | claude-code · codex · opencode · subagent-delegation |
| **GitHub** | github-pr-workflow · github-code-review · github-repo-management · github-issues · codebase-inspection |
| **Debugging** | triage-issue · invisible-elements-debugging |
| **Diagrams** | architecture-diagram · excalidraw |
| **MLOps** | vllm · llama-cpp · gguf |
| **MCP** | mcporter · native-mcp |

---

## Invocation

```bash
gh copilot -- -i "use github-pr-workflow to open a PR for this fix" --allow-all
gh copilot -- -i "use code-review to review the current branch" --allow-all
```

Or use the `/skill` shorthand when inside a `gh copilot` session.

---

## GH PR Workflow Rules

| Rule | Detail |
|------|--------|
| **Branch → PR → Squash/Merge** | Feature branches use `feat/`, `fix/`, `refactor/`, `docs/`, `ci/` naming |
| **Carlos merges** | Agent never merges — PR submitted for Carlos's review and merge |
| **Conventional Commits** | `type(scope): short description` — feat, fix, refactor, docs, test, ci, chore, perf |
| **CI auto-fix loop** | Detect failure → read logs → patch → push → re-check → repeat (max 3 attempts, then ask) |

---

## Installation

This plugin is part of the `awesome-hermes-skills` repo. After cloning the repo:

```bash
# Verify plugin is registered
gh copilot plugin list

# Should show: hermes-coding (enabled)
```

---

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — production-ready AI agent skills.*
