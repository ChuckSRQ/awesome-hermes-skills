---
name: last30days
version: "3.0.0"
description: Multi-query social search skill that researches any topic across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web. Synthesizes grounded summaries from the last 30 days.
argument-hint: 'last30days AI video tools, last30days best noise cancelling headphones'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
homepage: https://github.com/mvanhorn/last30days-skill
repository: https://github.com/mvanhorn/last30days-skill
author: mvanhorn
license: MIT
user-invocable: true
---

# last30days Research Skill

Research any topic across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, TruthSocial, GitHub, and the web from the last 30 days.

## Location
- SKILL.md and scripts installed at: `~/.claude/skills/last30days/`
- Main script: `~/.claude/skills/last30days/scripts/last30days.py`

## Runtime Preflight
Before running, resolve Python 3.12+ interpreter:
```bash
for py in python3.14 python3.13 python3.12 python3; do
  command -v "$py" >/dev/null 2>&1 || continue
  "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' || continue
  LAST30DAYS_PYTHON="$py"
  break
done
```

## Quick Run
```bash
"${LAST30DAYS_PYTHON}" ~/.claude/skills/last30days/scripts/last30days.py "your topic here" --emit=compact
```

## Setup (first run)
The skill auto-detects platform and walks through API configuration on first run.

## Key Sources
- Reddit (public JSON, no API key)
- X/Twitter (browser cookies via FROM_BROWSER=auto, xAI API key, or AUTH_TOKEN/CT0)
- YouTube (yt-dlp for transcripts)
- Hacker News, Polymarket, GitHub (via gh CLI if installed)
- TikTok/Instagram via ScrapeCreators (10k free calls)
- Bluesky via BSKY_HANDLE/BSKY_APP_PASSWORD
- Web search via Brave, Exa, or Serper

## Output
Briefings saved to `~/Documents/Last30Days/`
