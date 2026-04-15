---
name: vibe-log
description: Analyze Claude Code session logs, track productivity metrics, generate HTML reports. Use when analyzing coding sessions, reviewing session history, tracking productivity streaks, or generating visual session reports.
---

# VibeLog CLI Skill

Analyzes Claude Code prompts and produces HTML productivity reports.

## Core Commands

```bash
# Analyze current directory's sessions
vibelog analyze

# Generate HTML report
vibelog report --html

# View session history
vibelog sessions list

# Check streak/status
vibelog status
```

## For HTML Report Generation

1. Run `vibelog analyze` to process session data
2. Use `vibelog report --html` to generate visual report
3. Report outputs to stdout or specified path

## Key Features
- Session parsing from JSONL files
- Productivity metrics tracking
- Streak visualization
- HTML report generation with charts
