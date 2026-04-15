---
name: autonomous-ai-agents
description: Spawn and orchestrate autonomous AI subagents for Complex (Tier 3) tasks. Includes async/parallel execution patterns. For delegating coding tasks to Turing.
version: 3.0.0
author: Awesome Hermes
license: MIT
tags: [subagent, spawning, delegation, parallel, async, Turing]
---

# Autonomous AI Agents — Spawning and Orchestration

Spawning subagents for Complex (Tier 3) tasks. Based on Anthropic's finding: parallel subagent execution cut research time by 90%.

## The Architecture

**Lead Agent** = Orchestrator and reviewer. Thinks strategically, decomposes tasks, delegates to Turing, reviews output.
**Turing** = Execution specialist. Clean code craftsman. Receives briefs from the lead agent, executes precisely, delivers clean code.

**The user talks to the lead agent.** the lead agent hands off coding to Turing. Turing builds. the lead agent reviews and delivers.

```
User → Lead Agent → [delegate] → Turing → Code
                              ↑ review ↑
                          the lead agent reviews
```

## When to Delegate

**Tier 1 (Simple):** Do it yourself. One direct answer or action.
**Tier 2 (Medium):** Do it yourself. Coding tasks within your capability — use software-development, github, and other skills directly.
**Tier 3 (Complex):** Spawn Turing as a subagent for multi-step coding work that needs judgment during execution.

**Rule: When in doubt, go up a tier.** Under-investing is worse than over-investing.

## Spawn Turing as a Subagent

Use when you need a full agentic context — Turing can use tools, think through problems, and execute complex multi-step work autonomously.

```python
from hermes_tools import delegate_task

results = delegate_task(
    tasks=[
        {
            "goal": "Build the user authentication module for the API...",
            "context": "Brief from the lead agent. Build clean, tested code. Write to ~/project/src/auth/",
            "toolsets": ["terminal", "file", "github"]
        }
    ],
    max_iterations=30
)
```

**When to use:**
- Task needs judgment calls during execution
- Complex multi-step with dependencies
- Task requires coordination across multiple files or systems

## Turing Brief Template

Every task handed to Turing needs a complete brief:

```
GOAL: [the exact task — one sentence, one deliverable]
CONTEXT: [2-3 sentences on why this matters, what it connects to]
OUTPUT: [what file to write, what format, where to save it]
CONSTRAINTS: [tech stack, patterns to follow, patterns to avoid]
SUCCESS: [how the lead agent will judge if this is done]
```

**Example:**
```
GOAL: Add JWT authentication middleware to the Express.js API.
CONTEXT: This is for the property management portal. It needs to protect /api/protected routes. Tokens are issued by the auth service.
OUTPUT: Write to ~/prestige-tampa-living/server/middleware/auth.ts
CONSTRAINTS: Use jsonwebtoken library already in project. Follow existing middleware pattern in middleware/index.ts.
SUCCESS: Authenticated requests pass through. Unauthenticated requests return 401. At least 3 unit tests covering: valid token, expired token, missing token.
```

## Turing Workflow

1. **The lead agent decomposes** the request into a clear brief
2. **The lead agent delegates** to the subagent as a subagent
3. **Turing executes** using software-development, github, elegant-coder, and other skills directly
4. **Turing delivers** output with: what changed, what was created, what was tested
5. **The lead agent reviews** — approves or sends back with specific comments
6. **The lead agent delivers** to the user

## Subagent Profiles Quick Reference

| Profile | Best For | Tool Set |
|---------|---------|----------|
| Turing | Build, debug, test, validate, refactor | terminal, file, github, web |

## Effort Scaling for Subagents

| Task Type | Subagents | Tool Calls Each | Context |
|-----------|-----------|----------------|---------|
| Simple coding | Do it yourself | 3-10 | Focused |
| Medium coding | Do it yourself | 10-15 | Full brief |
| Complex multi-step | 1 Turing subagent | 15-30 | Complete context |

**Rule:** The lead agent (the lead agent) decides effort level. Don't let subagents self-allocate.

## Token Budget Guidance

Multi-agent burns tokens fast — 4x vs single chat, 15x for full multi-agent research.

**When to worry:**
- Complex (Tier 3) research tasks — always
- Medium (Tier 2) tasks with many sources — monitor
- Simple (Tier 1) tasks — don't monitor

**Token saving:**
- Use focused briefs (short context, specific goals)
- Save intermediate findings to shared memory
- Do Tier 1 and Tier 2 work yourself — don't spawn for simple tasks
- Prefer summary outputs when detail isn't needed

## Common Failure Modes

1. **Spawning when not needed** — Tier 1 and Tier 2 tasks don't need subagents. Do them yourself.
2. **Vague briefs** — subagent produces off-target output. Use the brief template above.
3. **No shared memory** — subagent output gets lost. Always specify output file.
4. **Sequential when parallel was possible** — check: "could these sub-tasks run independently?"
5. **Not reviewing Turing's work** — the lead agent reviews everything before delivering to the user.

## Self-Improvement Integration

When Turing underperforms:
1. Note the failure mode in the session log
2. Diagnose: was it the brief, the model, or the task complexity?
3. Adjust the brief format (more/less specific)
4. Report to the user so the workflow can be refined
