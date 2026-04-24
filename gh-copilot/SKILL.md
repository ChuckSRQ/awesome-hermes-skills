---
name: gh-copilot
description: "GitHub Copilot CLI plugin — 23 Hermes development skills wired into gh copilot. Use /skill or gh copilot -- -i 'use <skill-name>' to invoke any skill. Covers code review, TDD, debugging, GitHub workflows, AI agents, MLOps, and MCP."
version: 1.0.0
author: Carlos Graterol
license: MIT
metadata:
  github:
    plugin: hermes-coding
    skills_count: 23
    repository: https://github.com/ChuckSRQ/awesome-hermes-skills
---

# GH Copilot — GitHub Copilot CLI Plugin

This is a **plugin wrapper** skill. The actual skills are defined in the plugin manifest at `.github/plugin/plugin.json` and symlinked from `skills/`.

## Invocation

```bash
gh copilot -- -i "use github-pr-workflow" --allow-all
gh copilot -- -i "use code-review" --allow-all
gh copilot -- -i "use plan to analyze this codebase" --allow-all
```

Or via `/skill` shorthand inside a `gh copilot` session.

## Skills Directory

The 23 skills are located in `skills/` and correspond to the entries in `.github/plugin/plugin.json`. They are symlinked from `~/.hermes/skills/` and are managed by the Hermes skills system.

## Adding New Skills to the Plugin

To add a new skill to the plugin:

1. Ensure the skill exists in `~/.hermes/skills/`
2. Add an entry to `.github/plugin/plugin.json` under `"skills"`:
   ```json
   "./skills/my-new-skill"
   ```
3. Create a symlink or copy in `skills/my-new-skill/`
4. Update this SKILL.md to include the new skill in the count and category

## Plugin Structure

```
gh-copilot/
├── .github/
│   └── plugin/
│       └── plugin.json    # Plugin manifest — defines name, skills, version
├── skills/                # 23 skill directories (symlinked from ~/.hermes/skills/)
│   ├── code-review/
│   ├── claude-code/
│   ├── github-pr-workflow/
│   └── ... (23 total)
├── README.md             # This file (user-facing overview)
└── SKILL.md              # This file (technical reference)
```

## CI Auto-Fix Loop

When a PR check fails:

1. `gh pr checks` → identify failures
2. Read failure logs → understand the error
3. `patch/write_file` → fix the code
4. `git add . && git commit -m "fix: ..." && git push`
5. `gh pr checks --watch` → wait for green
6. Repeat (max 3 loops, then escalate to Carlos)

## Key Constraints

- Agent never merges — all merges are Carlos's responsibility
- All changes go through PR with squash merge
- Conventional Commits required: `type(scope): description`
- Branch naming: `feat/`, `fix/`, `refactor/`, `docs/`, `ci/`
