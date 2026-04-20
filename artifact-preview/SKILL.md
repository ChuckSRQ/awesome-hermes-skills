---
name: artifact-preview
description: "🪽 Write code, see it live, instantly. Claude-style artifacts with **smart persistent history**, live reload, inline editor, and one-click screenshots. Now with 'Save as New' and beautiful toasts. v4.2 — history actually works."
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

# Artifact Preview **v4.2** — Live HTML Preview + Reliable History 🏆

**The ultimate visual feedback loop for Hermes.** Generate beautiful, interactive HTML → instantly see it in a Chrome window → edit and iterate with live reload → **every version is automatically saved** so you can go back anytime.

## 🔥 What's New in v4.2

- Newest artifacts appear at the top of Recent dropdown
- Auto-save to history on server start
- "Saved to history" toast notifications
- **Save as New** button — preserve variations without losing your current live preview
- Pinned "● Current — Live" in dropdown for clarity

## Recommended Workflow (Copy-Paste This Pattern)

When the user asks you to **build, generate, update, or show** any visual artifact:

1. Generate **complete, polished, self-contained** HTML/CSS/JS (follow design standards below).
2. Always include a clear `<title>` and `<h1>` — this becomes the nice label in history.
3. Optionally add `<meta name="preview-mode" content="portrait|horizontal|full">`.
4. **Always** use this exact save pattern so history works perfectly:

```bash
cd ~/artifact-preview

cat > artifact.html << 'ENDOFHTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Clear Title Here</title>
    <!-- your amazing code -->
</head>
<body>
    <!-- content -->
</body>
</html>
ENDOFHTML

# This triggers save + archive + toast + live reload
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null
```

5. Then open the preview (auto mode recommended):

```bash
bash ~/artifact-preview/open-chrome.sh
```

**Pro move**: If you want to keep the current live preview unchanged but still save a variation, use **Save as New** in the editor toolbar — it archives without overwriting `artifact.html`.

---

## Design Standards

- **Complete, interactive, beautiful artifacts** (not skeletons)
- **Self-contained single HTML file**
- **Modern CSS** — flexbox/grid, CSS variables, rounded corners, transitions
- **Light-first** — warm white backgrounds (`#F8F7F4`) unless dark is clearly better
- **One accent color** — violet `#8B5CF6` at ~10% of visual space
- **Font**: Instrument Sans
- **WCAG 4.5:1 contrast** minimum on all text

### HTML template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Artifact Title</title>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Instrument Sans', -apple-system, sans-serif;
      background: #F8F7F4;
      color: #1A1A2E;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
  </style>
</head>
<body>
  <!-- your content -->
</body>
</html>
```

### Color palette (recommended)

```
--bg:        #FFFFFF or #F8F7F4 (warm white)
--surface:   #F0EEF6 (light lavender gray)
--text:      #1A1A2E (near-black)
--accent:    #8B5CF6 (violet)
--success:   #22C55E
--error:     #EF4444
--radius:    12px (cards), 8px (buttons), 6px (inputs)
--shadow:    0 4px 24px rgba(0,0,0,0.08)
```

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

### Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Preview UI |
| `/artifact.html` | GET | Raw artifact HTML |
| `/update` | POST | Save artifact.html + archive to history + broadcast reload |
| `/save-new` | POST | Archive as new version WITHOUT overwriting artifact.html |
| `/events` | GET | SSE stream for live reload + history updates |
| `/history/<filename>` | GET | Serve archived artifact |
| `/artifacts.json` | GET | History manifest |
| `/notify-open` | POST | Trigger browser auto-open |
| `/share-screenshot` | POST | Capture + save screenshot |
| `/check-open` | GET | Browser polls for pending auto-open |
| `/clear-open` | POST | Browser consumed the auto-open flag |

---

## Toolbar Controls

| Button | Action |
|--------|--------|
| **🪽 Hermes Preview** | Title label — "Preview" in violet accent |
| **Code / Split / Preview** | Tab group — toggle editor mode |
| **Recent dropdown** | Switch between live and archived artifacts |
| **Screenshot** | Retina capture → saves to Downloads + opens Preview |
| **Refresh** | Reload artifact immediately |

---

## History & Recent Dropdown

- History auto-populates on server start (captures initial `artifact.html`)
- Every `/update` or `/save-new` call archives a new entry
- Newest entries appear at **top** of dropdown
- Dropdown always shows "● Current — Live" at the top as a separator back to the live artifact
- Up to 15 entries are kept; oldest are pruned automatically
- Entries are labeled by `<title>` or first `<h1>`, with relative timestamp

**Save** (in editor) → overwrites `artifact.html` + archives the new version → live preview updates.

**Save as New** (in editor) → archives the editor's content as a new history entry → **does NOT overwrite `artifact.html`**, so your live preview stays intact.

---

## Troubleshooting

**Server address already in use (Errn 48)?**
Server is already running. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/` → 200 means running.

**Preview not updating?**
Click **Refresh** in toolbar (instant via SSE) or restart server: `pkill -f "artifact-preview/server.py" && cd ~/artifact-preview && python3 server.py &`

**Content clipping — preview card shows only half:**
CSS overflow stacking issue. Correct hierarchy: `body { overflow: auto }`, `#container { overflow: visible }`, `#preview-card { overflow: visible }`, `#artifact-frame { overflow: auto }`. Don't add `height: 100%` to `#preview-card`.

**Card appears full-width when it should be compact:**
First check: did you use `bash ~/artifact-preview/open-chrome.sh portrait` (correct) vs `open "http://localhost:8765"` (wrong — opens full tab)?

**Screenshot not working:**
Uses html2canvas inside the iframe. If it fails, toast suggests Cmd+Shift+4 as fallback. Screenshot saves to ~/Downloads + opens Preview app.

**Chrome window not opening (macOS):**
Grant Automation permissions: System Preferences → Privacy & Security → Automation → grant to Terminal.

**"Who's using Chrome?" profile picker:**
Use `do shell script "open -a 'Google Chrome'"` instead of `tell application "Google Chrome" to launch`.

**Dual-monitor full mode overflows:**
Use Swift's `NSScreen.main` (not Finder's `bounds of desktop`) for primary display only. The `.applescript` already does this.

**SSE connection lost:**
Live reload falls back to manual refresh. Banner auto-dismisses on reconnect. If persistent, restart server.

**History dropdown empty after copying files directly:**
Copying files to `artifact.html` via terminal does NOT auto-archive. Must use the editor Save button (POSTs to `/update`) or the `/save-new` endpoint.

---

## Launch Modes

| Mode | Command | Best For |
|------|---------|----------|
| Auto-detect | `bash ~/artifact-preview/open-chrome.sh` | Reads meta tag or uses heuristics |
| Portrait | `bash ~/artifact-preview/open-chrome.sh portrait` | Phone-sized window (~430×844) |
| Horizontal | `bash ~/artifact-preview/open-chrome.sh horizontal` | Video-sized window (~1240×720) |
| Full | `bash ~/artifact-preview/open-chrome.sh full` | Maximized to main display |

Always use `bash ~/artifact-preview/open-chrome.sh` — NOT `open "http://..."` which opens a full tab regardless of mode.

**Auto-detect heuristic:**
1. `<meta name="preview-mode" content="...">` (explicit, always wins)
2. `<nav>`/`<footer>`/`<header>` → full
3. Mobile viewport + narrow layout → portrait
4. Default → horizontal
