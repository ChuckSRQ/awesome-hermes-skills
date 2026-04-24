# Reviewed procedural-memory loop for Hermes

## Goal

Improve prompt policy through a human-reviewed workflow rather than automatic self-modification.

## Prompt-worthy failures

A failure is prompt-worthy when:
- the issue is instruction-shaped
- it generalizes beyond one conversation
- tooling or retrieval is not the main problem

A failure is not prompt-worthy when it is mainly:
- tool breakage
- missing auth
- retrieval failure
- environment issues
- temporary project state
- user-specific facts that belong in memory instead of policy

## Workflow

1. collect failed trajectories
2. generate a review packet
3. separate prompt failures from tool or retrieval failures
4. review candidate prompt deltas manually
5. apply approved changes in the real prompt source
6. rerun evals before shipping

## Never auto-learn

- secrets
- temporary task state
- one-off exceptions
- behavior inferred from broken tools
- irreversible policy changes without review

## Rule

Do not auto-patch the live system prompt from optimizer output.
