# Hermes LangMem memory architecture

## Goal

Upgrade Hermes from a basic LangMem integration into a structured local memory system that is easier to inspect, trust, and evolve.

## Lanes

### 1. Profile lane
Use one structured per-user document for durable identity and preference state.

Typical fields:
- name
- preferred_name
- timezone
- communication_style
- verbosity_preference
- preferred_tools
- active_projects
- dislikes
- correction_patterns
- recurring_workflows

Why it matters:
- stable user facts should not depend on keyword search
- prompt injection can use direct lookup instead of fuzzy retrieval

### 2. Fact / preference lane
Use the existing general memory rows for explicit facts and extracted durable preferences.

Recommended metadata:
- lane=`preferences`
- source_type=`conclude` or `sync_turn`
- first_seen_session_id
- last_seen_session_id
- confirmation_count
- tags

Why it matters:
- preserves explicit user-stated facts
- keeps background extraction reconcilable and inspectable

### 3. Episode lane
Store reusable successful interaction patterns separately from user facts.

Recommended row shape:
- `kind="episode"`
- `source="langmem-episode"`
- metadata lane `episodes`
- metadata source type `episode_sync`
- content stored as JSON

Why it matters:
- interaction patterns should not pollute stable user identity memory
- future procedural-memory workflows can inspect this lane separately

## Retrieval design

Keep the existing SQLite + FTS5 backend first.

Add Python-side reranking using local metadata before introducing embeddings.

Good first ranking inputs:
- `confirmation_count`
- `updated_at` recency bonus

Why it matters:
- gives materially better recall without infra migration
- keeps the system local and easy to debug

## Sync design

Debounce background extraction.

Pattern:
- keep a pending sync payload
- keep a deadline
- keep a lock
- let repeated rapid turns overwrite the pending payload
- process only the latest payload when the window expires

Why it matters:
- reduces wasted extraction passes on bursty chats
- avoids over-forming memory from tiny transactional turns

## Eval design

Measure four layers separately:
- extraction
- reconciliation
- retrieval
- injection usefulness

Use deterministic scenario families first:
- explicit preference writes
- preference correction
- cross-session recall
- lexical ambiguity in retrieval

Why it matters:
- lets you localize failures precisely
- avoids vague claims like "memory got better"

## Procedural-memory design

Treat prompt optimization as a reviewed workflow.

The first version should:
- load failed trajectories
- prepare a review packet
- identify where a prompt optimizer would later fit
- avoid auto-patching the live prompt

Why it matters:
- prevents opaque self-modifying behavior
- keeps policy changes human-reviewable

## Core principle

Memory should be:
- structured where stability matters
- provenance-aware where trust matters
- debounced where cost matters
- ranked where recall matters
- separated by lane where semantics differ
- evaluated where quality claims matter
- reviewed where policy changes matter
