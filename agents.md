# agents.md — Repo Operating Rules

*This file defines how changes get made to this repository.*

---

## The Four Skills

This repo contains exactly four skills — no more, no less.

| Skill | Path | Source | Status |
|-------|------|--------|--------|
| Artifact Preview | `artifact-preview/` | `~/.hermes/skills/dev-platform/workspace/artifact-preview/` | 🟢 Active |
| Deep Research | `deep-research/` | `~/.hermes/skills/ai-platform/deep-research/` | 🟢 Active |
| Agentic Benchmark Testing | `agentic-self-improvement/` | `~/.hermes/skills/productivity/agentic-self-improvement/` | 🟢 Active |
| GH Copilot | `gh-copilot/` | `~/.hermes/skills/github/gh-copilot/` | 🟢 Active |

---

## Frozen Skills

**Do not edit, delete, or refactor the following without explicit instruction:**

- `gh-copilot/` — GitHub Copilot CLI plugin. Contains 23 symlinked skills. Touching this breaks `gh copilot` invocation.
- `artifact-preview/` — Requires specific file structure and naming. Do not rename or restructure files inside.
- `deep-research/` — Knowledge base path (`~/research-skill-graph/`) is hardcoded. Do not change folder structure.
- `agentic-self-improvement/` — Benchmark paths and guidance patch locations are hardcoded. Do not move files inside.

---

## Repo Rules

### 1. Carlos merges. Never the agent.
Any structural change to this repo — skill additions, deletions, restructures, README updates — goes through a PR. Carlos reviews and merges. The agent creates the PR and stops.

### 2. Branch naming
```
feat/consolidate-to-4-skills  # new features
fix/skill-name                # bug fixes
docs/description              # documentation
```
No commit directly to `main`.

### 3. PR → Squash and merge
All PRs use squash merge. The merge commit message should follow Conventional Commits:
```
feat: add new skill X
fix: correct Y
refactor: restructure to 4 skills
```

### 4. No partial skill edits
Skills are copied from `~/.hermes/skills/` — they live there as the source of truth. Edits to skills in this repo do not sync back. If a skill needs changes, the source (`~/.hermes/skills/`) is updated first, then the change propagates here.

### 5. No new skills added without explicit instruction
This repo is intentionally limited to four. Do not add skills, no matter how useful they seem.

### 6. Deletions require a plan first
Before deleting anything, present the full list of what will be removed and get explicit confirmation. Deletions are permanent.

---

## GH Copilot Workflow Reference

### Branch → PR → Merge

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Create feature branch
git checkout -b feat/description

# 3. Make changes (skills, docs, etc.)
# ... agent uses file tools ...

# 4. Commit (Conventional Commits)
git add <files>
git commit -m "feat: short description"

# 5. Push
git push -u origin HEAD

# 6. Create PR (agent creates, Carlos merges)
gh pr create --title "feat: description" --body "## Summary..."
```

### Squash merge (Carlos's preference)
```bash
gh pr merge --squash --delete-branch
```

### Auto-fix CI failures
```
1. gh pr checks → identify failures
2. Read failure logs → understand the error
3. patch/write_file → fix the code
4. git add . && git commit -m "fix: ..." && git push
5. gh pr checks --watch → wait for green
6. Repeat (max 3 loops, then ask Carlos)
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Create branch | `git checkout -b feat/name` |
| Stage + commit | `git add . && git commit -m "type: message"` |
| Push | `git push -u origin HEAD` |
| Open PR | `gh pr create --title "..." --body "..."` |
| Check CI | `gh pr checks --watch` |
| Merge (squash) | `gh pr merge --squash --delete-branch` |

---

*Update this file when repo structure or rules change.*
