---
name: subagent-delegation-checkpoint
description: "After delegating to a subagent, verify the work was actually done before proceeding. Prevents 'completed' false positives from agents that finish fast but do little."
version: 1.0.0
author: Hermes Agent
---

# Subagent Delegation Checkpoint

## When to Use

After any `delegate_task` call returns with status "completed", perform these verification steps before treating the output as done.

## The Problem

Subagents can return "completed" status with minimal actual work — especially when:
- They read files but don't write substantive changes
- They complete in < 5 minutes on a task that should take longer
- They write placeholder or skeleton files
- They fail to actually implement what was specified

## Verification Checklist

### 1. Check file existence and size
```bash
# For page/component redesigns, check line counts
wc -l <file1> <file2> ...

# A real redesign of page.tsx should be 300+ lines
# A patched CSS should be 300+ lines
# If files are unchanged or suspiciously small, the work wasn't done
```

### 2. Check git diff (if in a repo)
```bash
git diff --stat
git diff <file>
```
This shows exactly what changed, not just that a file was touched.

### 3. Run the build
```bash
cd <project> && npm run build 2>&1 | tail -30
```
A real redesign may change line counts significantly. A partial/redundant change often causes build failures.

### 4. Spot-check key sections
Read a specific line range from modified files to confirm the new design is actually present (e.g., search for a new color variable, new section name, or new layout class).

## Decision Tree After Check

| Check Result | Action |
|---|---|
| Files updated, substantive changes present | Proceed |
| Files touched but no real changes | Re-delegate with stricter brief, or implement directly |
| Files not touched at all | Implement directly yourself |
| Build fails | Fix errors or re-delegate |

## Anti-Pattern This Prevents

> Subagent completed in 270 seconds. Checked — only 2 small CSS strings were patched. page.tsx, Navigation.tsx, Footer.tsx, ContactForm.tsx were all untouched. Had to implement the full redesign directly.

## Usage Note

This is a lightweight verification, not a full code review. The goal is to catch gross failures (nothing done) vs. actual work. Don't over-engineer — just check 2-3 signals (file size, build pass, git diff).
