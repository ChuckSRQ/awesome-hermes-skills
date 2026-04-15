---
name: research-skill-graph
description: A local research engine using Claude Code + Obsidian + a network of markdown files. Takes ONE research question and produces multi-angle analysis through 6 forced lenses.
trigger: "use when the user says 'research' or asks to investigate a topic deeply, or when he says to use the research skill graph system"
---

# Research Skill Graph

A local research engine using Claude Code + Obsidian + a network of markdown files. Takes ONE research question and produces multi-angle analysis through 6 forced lenses.

## Trigger
Use when the user says "research" or asks you to investigate a topic deeply, or when he says to use the "research skill graph" or "skill graph" system.

## How It Works

The system is a folder of interconnected markdown files at `~/Obsidian/research-skill-graph/`:

```
research-skill-graph/
├── index.md                    # Command center — paste your question here
├── research-log.md            # Chronological record of all projects
├── methodology/
│   ├── research-frameworks.md  # Pick approach based on question type
│   ├── source-evaluation.md    # 5-tier trust system
│   ├── synthesis-rules.md      # Combine findings without losing nuance
│   └── contradiction-protocol.md
├── lenses/                     # The core engine — 6 ways to rethink any question
│   ├── technical.md            # Data, numbers, mechanisms
│   ├── economic.md             # Money, incentives, who profits
│   ├── historical.md           # Patterns, precedents, context
│   ├── geopolitical.md        # Countries, power, alliances
│   ├── contrarian.md           # What if consensus is wrong?
│   └── first-principles.md     # Rebuild from fundamental truths
├── projects/                   # One subfolder per research project
├── sources/                    # Source templates
└── knowledge/
    ├── concepts.md             # Mental models — compounds over time
    └── data-points.md          # Verified numbers — compounds over time
```

## Execution Steps

### Phase 1: Setup
1. Create project subfolder: `projects/[project-name]/`
2. Create `projects/[project-name]/index.md` — define scope, question, time horizon, output goal
3. Read `index.md` — understand the system structure
4. Read `research-frameworks.md` — pick approach based on question type
5. Read `source-evaluation.md` — know what counts as good evidence

### Phase 2: Research (6 Lenses)
Delegate to subagents. **IMPORTANT:** `delegate_task` max_concurrent_children = 3. Split 6 lenses into 2 batches.

**Batch 1** (3 lenses): technical + economic + historical
**Batch 2** (3 lenses): geopolitical + contrarian + first-principles

Per batch, pass this context to each subagent:
```
Hermes ecosystem: https://github.com/ksimback/hermes-ecosystem
Research vault: ~/Obsidian/research-skill-graph/
Output folder: ~/Obsidian/research-skill-graph/projects/[project-name]/
```

Each lens task should research the question through ONE specific angle only and return structured findings.

### Phase 3: Synthesis
1. Read `contradiction-protocol.md` — document disagreements between lenses
2. Read `synthesis-rules.md` — combine everything into final outputs
3. Produce all 5 output files:
   - `executive-summary.md` — 500 words max, key findings + tensions
   - `deep-dive.md` — full analysis organized by lens with contradictions
   - `key-players.md` — people/orgs/countries that matter
   - `open-questions.md` — what we STILL don't know (as important as findings)
4. Update `research-log.md` — log the project with key findings
5. Update `knowledge/concepts.md` — add 3-5 new concepts discovered
6. Update `knowledge/data-points.md` — add verified numbers with source attribution

## Key Principles

- **Contradictions are features.** Don't resolve them — surface them. The tension between lenses IS the insight.
- **6 lenses, 6 different researchers.** Technical and contrarian should disagree. That disagreement is where insight lives.
- **Always cite source tiers.** Only Tier 1-2 for claims. Flag Tier 3+ as lower confidence.
- **Document what you don't know.** `open-questions` is as important as `executive-summary`.
- **Knowledge compounds.** Update `concepts.md` and `data-points.md` after every project. The 10th project starts from everything learned before.

## Vault Location
`~/Obsidian/research-skill-graph/`

## Tips
- **Delegation constraint:** `delegate_task` max_concurrent_children = 3. Always split 6 lenses into 2 batches.
- Point Claude Code at the vault folder for full power — it reads/writes directly, graph evolves itself
- In Obsidian, open the vault to see the graph view — spot disconnected nodes (research gaps)
- Compound mode: link open-questions from one project into the index of the next
- For a clean slate: only upload `methodology/` and `lenses/` — same system, fresh brain
- After research: ALWAYS update research-log, concepts, and data-points — that's how the system compounds

## Reference
Full system design documented in: `~/Obsidian/research-skill-graph/index.md`
