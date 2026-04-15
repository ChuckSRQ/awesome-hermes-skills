---
name: subagent-delegation
description: Rules and procedures for delegating work to subagents (OpenClaude via Turing, Claude Code, Codex, etc.) — branch management, interruption handling, and post-subagent verification.
version: 1.0.0
author: Hermes Agent
tags: [delegation, subagent, github, branch-management]
---

# Subagent Delegation Rules

These rules apply whenever work is delegated to a subagent via `delegate_task`, Turing/OpenClaude, Claude Code, or any other autonomous agent that modifies code or creates git branches.

**Load this skill whenever delegating significant work to a subagent.**

---

## Pre-Delegation Checklist

Before launching a subagent:

1. Check current branch state — `git branch -a && git status`
2. Determine the correct branch — Does an existing branch already cover this work? Create new only if genuinely new scope.
3. Decide: one agent or many? If multiple subagents will touch the same files, use ONE agent for the whole task.
4. Name the branch explicitly in the subagent prompt.

---

## Branch Rules

- **ONE branch per logical unit of work.** If a task has multiple parts, delegate to ONE subagent for everything, or have the parent consolidate results onto a single branch.
- **Never run parallel subagents that each create their own branch for the same goal.** Parallelism is fine for independent workstreams with separate branch names.
- **Specify branch name explicitly in the prompt.** e.g., "Branch from main, name your branch `fix/your-issue`."

---

## Subagent Prompt Requirements

Every subagent prompt must include ALL of:

```
- Branch from main, name your branch `fix/...` (or `feat/...`, `docs/...`)
- Run build and fix all errors before committing
- Create PR via GitHub when done
- Report back: what was done, what files were changed, what remains
```

---

## Interruption Handling

If a subagent is interrupted (not completed):

1. `git status` + `git diff --stat` — see what files were modified
2. `git stash` any uncommitted changes immediately
3. Verify build still passes
4. If work is on a separate branch: cherry-pick or merge onto the correct branch
5. The lead agent owns consolidation — do not leave partial work scattered across branches

---

## Post-Subagent Checklist

Before telling the user a subagent is done:

- [ ] Build passes cleanly
- [ ] All modified files are on the correct branch
- [ ] PR created and push succeeded
- [ ] No orphaned branches with partial work
- [ ] Exact summary of what was changed

---

## Merging Rules

- **Subagents never merge PRs.** The user merges their own PRs.
- Do not close, merge, or delete PRs without explicit user permission.

---

## Credential Error Handling

If `git push` fails with `git: 'credential-gh' is not a git command`:

- The push still succeeds to the remote — the error is only about credential caching
- Check `git remote -v` to confirm remote URL is correct (HTTPS, not SSH)
- PR creation via `gh pr create` may also fail if `gh` is not authenticated
- In all cases, verify the branch exists on remote before reporting success
