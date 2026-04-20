# Agent Operating Rules

## Skills Sourcing

All skills originate from **Hermes** — the skills library is maintained by Hermes and delivered to this repo. Agents do not create skills from scratch; they work with the skills provided by the Hermes system.

## The Three Locations

| Location | Purpose |
|---|---|
| `~/.hermes/skills/` | **Hermes skills directory.** Where Hermes actually reads and uses skills at runtime. **DO NOT EDIT.** |
| Local repo (`/users/carlosmac/awesome-hermes-skills/`) | Working copy. Agents operate here. |
| GitHub repo (`github.com/carlosmac/awesome-hermes-skills`) | Source of truth. All changes land here via PR. |

## Editing Workflow

**Rule: NO DIRECT EDITS. NO CHANGES TO HERMES DIRECTLY.**

When an agent needs to modify a skill:

1. **Create a branch** from the current main branch
2. **Make edits** in the local repo on that branch
3. **Open a Pull Request** — all changes require human review and approval
4. **Merge** — only after human review passes; the agent never self-approves

## Why This Matters

Hermes has its own skills directory (`~/.hermes/skills/`) that it uses at runtime. The awesome-hermes-skills repo is a **mirror and working copy** — it is not Hermes itself. Editing files in the repo does not immediately affect Hermes, which is intentional. Changes must flow through the PR review process so they are reviewed, tested, and approved before being merged.

## Summary

- Work happens in the **local repo only**
- Changes to Hermes skills directory are **forbidden** — that is Hermes's own working space
- All modifications go through **branch → PR → human review → merge**
- The agent's job is to prepare and propose changes; humans approve and merge
