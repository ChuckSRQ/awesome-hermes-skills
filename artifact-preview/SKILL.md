---
name: artifact-preview
description: "🪽 Magic. Fast. Generate HTML → it opens in Chrome for the human to see. Every version auto-saved. For showing humans what you built — not for agents to read."
triggers:
  - make
  - build
  - show
  - create
  - generate
  - visual
  - interactive
  - dashboard
  - app
  - website
  - demo
  - component
  - page
  - ui
  - form
  - widget
  - chart
---

# Artifact Preview **v4.2** — Live HTML Preview 🏆

**Magic. Fast. Generate HTML → it opens in Chrome for the human to see. Every version auto-saved.**

## What This Is

This skill is for **showing the human** what you built — a UI, a chart, a page, a result. Visually. Instantly.

It is **not** for agents to read or analyze content. The Chrome window exists for human eyes only. If you need to extract data, do that directly from the source — not from the preview.

## How to Use

1. Generate **complete, polished, self-contained** HTML/CSS/JS (see Design Standards below).
2. Save it using this exact pattern:

```bash
cd ~/artifact-preview

cat > artifact.html << 'ENDOFHTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Clear Title Here</title>
</head>
<body>
    <!-- your content -->
</body>
</html>
ENDOFHTML

# Saves + archives + live reload
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null
```

3. Open the preview so the human can see it:

```bash
bash ~/artifact-preview/open-chrome.sh
```

Always include `<title>` and `<h1>` — history labels depend on them.

**Pro move**: Want to save a variation without losing the current live preview? Use **Save as New** in the editor toolbar — it archives the variation without overwriting `artifact.html`.

---

## Design Standards

- **Complete, interactive, beautiful** — not skeletons, not placeholders
- Self-contained single HTML file
- Light-first: `#F8F7F4` warm white background, `#8B5CF6` violet accent at ~10%
- Instrument Sans font, WCAG 4.5:1 contrast

---

## Server Commands

```bash
# Start server (background)
cd ~/artifact-preview && python3 server.py &

# Stop server
pkill -f "artifact-preview/server.py"

# Verify running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# Returns 200 if running
```

### Endpoints

| Endpoint | Method | What it does |
|----------|--------|--------------|
| `/update` | POST | Save artifact.html + archive + live reload |
| `/save-new` | POST | Archive as new version WITHOUT overwriting artifact.html |
| `/` | GET | Preview UI |
| `/artifact.html` | GET | Raw artifact HTML |
| `/artifacts.json` | GET | History manifest |
| `/events` | GET | SSE stream for live reload + history updates |
| `/history/<filename>` | GET | Serve archived artifact |

---

## Toolbar Controls

| Button | Action |
|--------|--------|
| **🪽 Hermes Preview** | Title label |
| **Code / Split / Preview** | Toggle editor mode |
| **Recent dropdown** | Switch between live and archived artifacts |
| **Screenshot** | Retina capture → saves to Downloads + opens Preview |
| **Refresh** | Reload artifact immediately |

---

## History

History auto-populates on server start. Every `/update` or `/save-new` archives a new entry. Newest appear at top. Up to 15 kept.

**Save** → overwrites `artifact.html` + archives → live preview updates.

**Save as New** → archives editor content as new entry → **does NOT overwrite** `artifact.html`.

---

## Troubleshooting

**Server address already in use (Errn 48)?**
Server is already running. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/` → 200 means running.

**Preview not updating?**
Click **Refresh** in toolbar (instant via SSE) or restart server: `pkill -f "artifact-preview/server.py" && cd ~/artifact-preview && python3 server.py &`

**Content clipping — preview card shows only half:**
CSS overflow stacking. Correct: `body { overflow: auto }`, `#container { overflow: visible }`, `#preview-card { overflow: visible }`, `#artifact-frame { overflow: auto }`. Don't add `height: 100%` to `#preview-card`.

**Card appears full-width when it should be compact:**
Did you use `bash ~/artifact-preview/open-chrome.sh portrait` (correct) vs `open "http://localhost:8765"` (wrong — opens full tab)?

**Screenshot not working:**
Uses html2canvas inside iframe. If it fails, toast suggests Cmd+Shift+4 as fallback.

**Chrome window not opening (macOS):**
Grant Automation permissions: System Preferences → Privacy & Security → Automation → grant to Terminal.

**"Who's using Chrome?" profile picker:**
Use `do shell script "open -a 'Google Chrome'"` instead of `tell application "Google Chrome" to launch`.

**SSE connection lost:**
Live reload falls back to manual refresh. Restart server if persistent.

**History dropdown empty after copying files directly:**
Terminal writes don't auto-archive. Use the editor Save button (POSTs to `/update`) or `/save-new` endpoint.

---

## Launch Modes

```bash
bash ~/artifact-preview/open-chrome.sh           # auto-detect
bash ~/artifact-preview/open-chrome.sh portrait   # phone window ~430×844
bash ~/artifact-preview/open-chrome.sh horizontal # video window ~1240×720
bash ~/artifact-preview/open-chrome.sh full       # maximized
```

Always use `bash ~/artifact-preview/open-chrome.sh` — NOT `open "http://..."` which opens a full tab regardless of mode.

**Auto-detect heuristic:**
1. `<meta name="preview-mode" content="...">` (explicit, always wins)
2. `<nav>`/`<footer>`/`<header>` → full
3. Mobile viewport + narrow layout → portrait
4. Default → horizontal
