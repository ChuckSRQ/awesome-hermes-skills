---
name: memory-overflow-to-obsidian
description: Migrate structured data from the memory tool to Obsidian when memory gets full or needs hierarchy. Use when memory exceeds ~70% or when flat entries become unwieldy.
tags: ["memory", "obsidian", "workflow"]
---

# Memory Overflow to Obsidian

Use when: memory is >70% full, needs structure/hierarchy, or the user asks for "folders" in memory.

## Step 1 — Identify what needs to move

Group related info into categories (e.g., for a business: contacts, services, standards, templates).

## Step 2 — Create Obsidian notes

```
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

cat > "$VAULT/03-Notes/Name-Category.md" << 'ENDNOTE'
# Title

Content.
ENDNOTE
```

Use `03-Notes` for reference info, `04-Meetings` for recurring meeting notes, `02-Tasks` for project tasks.

## Step 3 — Update memory to point to Obsidian

Replace the migrated entries with a single reference line:
```
## [Topic] — See Obsidian
- Full info at: ~/Obsidian/03-Notes/[Topic]-*.md
```

## Key Lessons Learned

- Memory `replace` and `remove` require exact `old_text` matching — include enough context
- Memory has NO folder/hierarchy structure — flat entries only
- Memory tool does NOT manage contacts in other apps (e.g., WhatsApp) — it only sends messages
- Obsidian has no character cap and supports full markdown structure
- Obsidian notes persist and are searchable across sessions
- On macOS: home is `$HOME`, NOT `/home/<username>`. Writing to `/home/<username>/` silently fails. Use `~/Obsidian/...` (shell expands `~` correctly) or the full macOS path.
- Memory `replace` fails if the result would exceed ~2,200 chars — even if you're replacing a large entry with a small one. Workaround: `remove` the large entry first, then `add` or `replace`.

## Consolidation Workflow

When cleaning up scattered files and consolidating into new Obsidian notes:

1. Read all existing source files first
2. Write the merged destination file (delete content duplications)
3. Delete the old source files (rm)
4. Update `00-Vault Index.md` to reflect new structure
5. Only then clear and rebuild short-term memory

## When to Use Obsidian Instead of Memory

| Use | Memory | Obsidian |
|-----|--------|----------|
| Quick facts, preferences, corrections | Yes | No |
| Structured reference (contacts, services, standards) | No | Yes |
| Templates, checklists | No | Yes |
| Session state / TODO progress | No | No |
