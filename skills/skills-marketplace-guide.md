---
name: skills-marketplace-guide
description: Navigate the skills marketplace (mattpocock, ComposioHQ, Superpowers, anthropics) — install skills, avoid dead paths, handle the .agents/skills/ quirk.
triggers:
  - install a skill
  - add a skill
  - skills marketplace
  - npx skills
  - mattpocock skills
  - ComposioHQ skills
---

# Skills Marketplace Guide

## Installing Skills via npx

Use the `--yes` flag to skip interactive prompts:

```bash
npx skills@latest add REPO/PATH --yes
```

## Where Skills Actually Land

The `npx skills@latest add` command clones repos and places skills in `.agents/skills/` (universal agent format) — NOT directly in your main skills directory.

**After installing, always check and copy:**

```bash
# Check what was installed
ls ~/.hermes/skills/.agents/skills/

# Copy to main skills directory
cp -r ~/.hermes/skills/.agents/skills/SKILL_NAME ~/.hermes/skills/
```

## Repo-Specific Path Patterns

### mattpocock/skills
```bash
npx skills@latest add mattpocock/skills/SKILL_NAME --yes
# Example: npx skills@latest add mattpocock/skills/grill-me --yes
```

### ComposioHQ/awesome-claude-skills
Full subdirectory paths required — top-level names don't work:
```bash
# These work:
npx skills@latest add ComposioHQ/awesome-claude-skills/document-skills/pdf --yes
npx skills@latest add ComposioHQ/awesome-claude-skills/document-skills/docx --yes
npx skills@latest add ComposioHQ/awesome-claude-skills/changelog-generator --yes

# These DON'T work (no subdirectory specified):
npx skills@latest add ComposioHQ/awesome-claude-skills/pdf --yes
npx skills@latest add ComposioHQ/awesome-claude-skills/dependency-auditor --yes
```

### anthropics/skills
```bash
npx skills@latest add anthropics/skills/SKILL_NAME --yes
```

### Superpowers (obra/superpowers)
Superpowers skills are often NOT installable via the npx CLI. If the npx route fails, install directly from raw GitHub:
```bash
mkdir -p ~/.hermes/skills/SKILL_NAME
curl -s https://raw.githubusercontent.com/obra/superpowers/main/skills/SKILL_NAME/SKILL.md > ~/.hermes/skills/SKILL_NAME/SKILL.md
# Example: brainstorming, systematic-debugging, test-driven-development
```

## Known Dead Paths

Some skills listed in skill directories or articles don't exist at their stated paths:
- `anthropics/skills/auto-commit` — does not exist
- `ComposioHQ/awesome-claude-skills/dependency-auditor` — does not exist (removed/renamed)
- `ComposioHQ/awesome-claude-skills/xlsx` — requires `document-skills/xlsx` subdirectory

**Always verify after install:** `ls ~/.hermes/skills/.agents/skills/SKILL_NAME`

## Skill File Location Conventions

Skills can live in:
- `~/.hermes/skills/` — flat .md files (e.g., `skill-name.md`)
- `~/.hermes/skills/` — directories with `SKILL.md` inside (e.g., `skill-name/SKILL.md`)
- `~/.hermes/skills/.agents/skills/` — universal format, needs copying

## Post-Installation Checklist

1. Copy from `.agents/skills/` to main skills directory
2. Verify: `ls ~/.hermes/skills/SKILL_NAME/SKILL.md`
3. Test by referencing the skill in a new task
4. If skill has associated scripts/templates, check the `references/` or `scripts/` subdirectory

## SkillsMP Marketplace

For finding skills: https://skillsmp.com — treat it like package management. Search before building new skills.
