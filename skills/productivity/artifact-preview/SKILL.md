---
name: artifact-preview
description: Generate HTML/CSS/JS artifacts and open live previews instantly. Auto-opens browser after writing artifact. Three launch modes — Portrait (phone), Horizontal (video), Full (maximized). Card auto-fits to content size. No mode toggle. Includes screenshot-to-Preview sharing and inline HTML editor. v3.0.
triggers:
  - make
  - build
  - show
  - create
  - generate
  - visual
  - interactive
  - app
  - dashboard
  - form
  - game
  - component
  - widget
  - page
  - ui
  - website
  - demo
  - chart
  - video
  - plugin
---

# Artifact Preview v3.0 — Live HTML/CSS/JS Preview

Generates complete, polished HTML/CSS/JS, saves it, and **automatically opens the browser** — no manual steps. Three launch scripts: **Portrait** (`bash ~/artifact-preview/open-chrome.sh portrait`) opens a phone-sized window (~430×844), **Horizontal** (`bash ~/artifact-preview/open-chrome.sh horizontal`) opens a video-sized window (~1240×720), **Full** (`bash ~/artifact-preview/open-chrome.sh full`) opens a maximized Chrome window. The card is purely responsive (max-width 960px, centered, rounded) — no mode toggle, no state. The window size IS the mode.

## One-time setup

```bash
mkdir -p ~/artifact-preview
chmod +x ~/artifact-preview/open-chrome.sh
chmod +x ~/artifact-preview/share-screenshot.py
# Already done if using existing install
```

## The complete workflow

### Step 1 — Ensure server is running

```bash
# Start (or restart) the server — background process
pkill -f "artifact-preview/server.py" 2>/dev/null
cd ~/artifact-preview && python3 server.py &
# Verify
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# 200 = running
```

### Step 2 — Generate and save artifact + auto-open

Use `terminal` with heredoc for the HTML (handles special characters better than write_file for large content):

```bash
cat > ~/artifact-preview/artifact.html << 'ENDOFFILE'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Artifact</title>
  <!-- inline CSS/JS only, no external deps except Google Fonts -->
</head>
<body>
  <!-- your content -->
</body>
</html>
ENDOFFILE
```

After saving, **auto-open the browser**:

```bash
# For phone/mobile artboards → portrait window (~430×844)
bash ~/artifact-preview/open-chrome.sh portrait

# For video/landscape content → horizontal window (~1240×720)
bash ~/artifact-preview/open-chrome.sh horizontal

# For everything else → maximized Chrome window
bash ~/artifact-preview/open-chrome.sh full
```

**IMPORTANT**: Always use `bash ~/artifact-preview/open-chrome.sh` — NOT `open "http://..."` which opens a full tab regardless.

**That's it.** Browser opens automatically. Artifact is live.

### Step 3 — Update and see changes instantly

Overwrite `~/artifact-preview/artifact.html`, then click **Refresh** in the toolbar. The browser auto-reloads via SSE (no polling).

---

## Launch guide

| Content type | Launch command | Result |
|-------------|---------------|--------|
| Phone/mobile artboards, Instagram, tall UI | `bash ~/artifact-preview/open-chrome.sh portrait` | Phone-sized window, bounds {60,60,490,904} |
| Video, landscape layouts, wide components | `bash ~/artifact-preview/open-chrome.sh horizontal` | Video-sized window, bounds {60,60,1300,740} |
| Full websites, dashboards, complete layouts | `bash ~/artifact-preview/open-chrome.sh full` | Maximized Chrome window (screen bounds) |

**Default is `full`** — calling `open-chrome.sh` with no argument opens maximized.

There is **no mode toggle** in the toolbar. The window size IS the mode. The card is responsive and adapts to whatever window it's in.

### Auto-fit to content

The card automatically shrinks to hug small artifacts (widgets, charts, plugins). On iframe load, `autoFitCard()` reads the artifact's `scrollWidth`:

- Content < 900px → card shrinks to `contentWidth + 64px` padding (e.g. a 300px widget → 364px card)
- Content >= 900px → card fills to 960px (assumes full-width responsive layout)
- Editor opens → auto-fit resets, card expands to 1100px
- Editor closes → auto-fit re-runs

This means small components look centered and contained, while full websites fill the window naturally.

---

## Toolbar controls

| Button | What it does |
|--------|-------------|
|| **🪽 Hermes Preview** | Title label (not a button) — "Preview" in violet accent |
| **Code** | Open editor, full-width code view — iframe hidden, editor fills card |
| **Split** | Open editor, split view — iframe left 50%, editor right 50% |
| **Preview** | Close editor, preview-only mode — iframe fills card, editor hidden |
| **Screenshot** | Captures preview as PNG → saves to ~/Downloads + opens Preview (Share button available) |
| **Refresh** | Reload the artifact immediately |

**Keyboard shortcuts** (when preview tab is focused):
- `Cmd/Ctrl + Shift + E` — toggle HTML editor (Code ↔ Preview)
- `Cmd/Ctrl + Shift + S` — save from editor
- `Cmd/Ctrl + Shift + R` — refresh preview

---

## HTML Editor

The editor is controlled by the **Code / Split / Preview** tab group in the toolbar:

- **Code tab** — editor-panel fills full card width; iframe hidden
- **Split tab** — iframe LEFT 50% + editor RIGHT 50% (artifact preview left, code editor right)
- **Preview tab** — iframe full card width; editor hidden (back to preview-only mode)

Source is loaded lazily on first editor open (not on every tab switch).

The **HTML button is no longer in the toolbar** — the Code/Split/Preview tabs fully control editor visibility.

- **Copy** — copy source to clipboard
- **Save** — POSTs to `/update` endpoint (server saves to artifact.html) + reloads preview

The iframe IS the preview in all modes — no separate editor preview iframe. In split mode, the left pane shows the actual artifact.html URL.

Keyboard: `Cmd+Shift+E` toggle editor, `Cmd+Shift+S` save, `Cmd+Shift+R` refresh.

---

## Screenshot + Share workflow

1. Click **Screenshot** button in toolbar
2. Preview captures and opens in Preview app (in ~/Downloads too)
3. In Preview, click the **Share button** (top right) → AirDrop, Messages, Mail, etc.

This approach is more reliable than programmatic share sheets and gives you full macOS sharing options.

---

## File locations

```
~/artifact-preview/
  server.py          ← Python HTTP server with SSE (run once, stays in background)
  open-chrome.sh     ← Browser launcher (portrait / horizontal / full window)
  share-screenshot.py ← Saves screenshot to Downloads + opens Preview
  index.html         ← UI wrapper with toolbar (don't edit)
  artifact.html      ← Your generated artifact (overwrite each time)
  history/           ← Backup of past artifacts
```

---

## Design standards

- **Complete code** — Not a skeleton. Real working interactive app/widget.
- **Modern CSS** — Flexbox/grid, CSS variables, rounded corners, smooth transitions
- **Interactive** — Buttons work, inputs respond, animations play
- **Self-contained** — One HTML file, inline CSS/JS, no build step, no external deps except Google Fonts
- **Light-first** — Default to white/warm backgrounds. Dark only when content demands it
- **One accent color** — Saturated accent at ~10% of visual space. Violet (#8B5CF6) is the current theme accent.
- **Font**: Instrument Sans — Clean, modern. Google: `https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap`
- **WCAG 4.5:1 contrast** minimum on all text

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

### HTML template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artifact</title>
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

---

## Server commands

```bash
# Start server (background)
cd ~/artifact-preview && python3 server.py &

# Stop server
pkill -f "artifact-preview/server.py"

# Verify running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# Returns 200 if running

# Check which port
lsof -i :8765 | grep LISTEN
```

---

## Troubleshooting

**Preview not updating?**
- Click **Refresh** in the toolbar — instant reload via SSE, no waiting
- If that doesn't work: `pkill -f "artifact-preview/server.py" && cd ~/artifact-preview && python3 server.py &`

**Content clipping — preview card shows only half the content, even when scrolling:**
This is a CSS overflow stacking issue. The correct overflow hierarchy (discovered through debugging) is:
- `body { overflow: auto }` — body is the scroll container
- `#container { overflow: visible }` — container lets card grow beyond viewport
- `#preview-card { overflow: visible }` — card clips nothing
- `#artifact-frame { overflow: auto }` — iframe scrolls its own content internally

Common mistake: adding `height: 100%` to `#preview-card` — this resolves against the container's height (which is `auto`), not the viewport. Let `overflow: visible` let the card grow beyond it.

**Card appears full-width when it should be compact:**
Always open with `bash ~/artifact-preview/open-chrome.sh portrait` (or `horizontal` for wide content) — NOT `open "http://localhost:8765"`. The `open` command opens a full Chrome tab. The AppleScript launcher sets the Chrome window bounds — that IS the compact mode.

**Debugging pitfall — CSS vs launcher:**
If the card appears full-width, FIRST check whether you used `open` (wrong) vs `bash ~/artifact-preview/open-chrome.sh portrait` (correct). Don't waste time tweaking CSS — the issue is the Chrome window size, not the card CSS. The browser automation tool (browser_navigate) opens tabs at full width too, so it won't reproduce the compact-window experience.

**editor-open class leaking into Preview mode:**
If `setEditorTab('preview')` doesn't remove `editor-open` from body, the card stays at editor width (1000px) instead of 640px. Fix: `setEditorTab` removes ALL body classes first (`editor-open`, `editor-code`, `editor-split`, `editor-preview-tab`), then adds only the new one.

**artifact.html not found:**
- The server serves a "No artifact loaded" message — make sure you wrote `artifact.html` (not `index.html`)

**Screenshot not working:**
- The screenshot feature uses html2canvas running inside the iframe — all CSS/fonts/images render correctly
- If it fails, the error toast will suggest Cmd+Shift+4 as fallback
- Screenshot captures the artifact at device DPR (capped at 2x) for sharp output
- Result saves to ~/Downloads + opens in Preview app (Share button available there)

**Chrome window not opening:**
- Make sure `open-chrome.applescript` is executable: `chmod +x ~/artifact-preview/open-chrome.applescript`
- Use `osascript ~/artifact-preview/open-chrome.applescript portrait` directly (the .sh wrapper just calls this)
- **Important**: AppleScript variable name `mode` conflicts with Chrome's dictionary — always use a different variable name
- **macOS Automation permissions**: the first time you run this, macOS will prompt for Automation/Accessibility access. Grant Terminal (or your terminal app) permission to control Google Chrome in System Preferences → Privacy & Security → Automation.

**AppleScript argument passing:**
- `#!/usr/bin/env osascript` shebang does NOT pass CLI arguments — use explicit `osascript /path/to/script.applescript "$arg"` instead
- Variable name `mode` is reserved in Chrome's OSA dictionary — rename to avoid it
- Correct pattern for the `.applescript` file:

```applescript
on run argv
    set rawMode to "full"
    if (count of argv) > 0 then set rawMode to item 1 of argv

    -- Normalize
    try
        set theMode to do shell script "printf %s " & quoted form of rawMode & " | tr '[:upper:]' '[:lower:]'"
    on error
        set theMode to rawMode
    end try

    tell application "System Events"
        set chromeRunning to (exists (processes where name is "Google Chrome"))
    end tell

    if not chromeRunning then
        tell application "Google Chrome" to launch
        delay 0.6
    end if

    tell application "Google Chrome"
        activate
        make new window
        delay 0.15

        if theMode is "portrait" then
            set bounds of front window to {60, 60, 490, 904}
        else if theMode is "horizontal" then
            set bounds of front window to {60, 60, 1300, 740}
        else
            tell application "Finder"
                set screenBounds to bounds of window of desktop
            end tell
            set bounds of front window to screenBounds
        end if

        set URL of active tab of front window to "http://localhost:8765"
    end tell
end run
```

**Editor Save not working:**
- Save POSTs to server — server must be running. If server doesn't support it, Save falls back to downloading the file.

**SSE connection lost (banner shows):**
- Live reload falls back to manual refresh. Banner auto-dismisses when reconnected.
- If persistent: restart server.

**iframe contentDocument not ready on load event:**
- The `load` event fires before `contentDocument` is accessible. Screenshot function should poll with ~100ms intervals up to 20 attempts before attempting SVG capture. Screenshot button can be enabled immediately — the click handler does its own readiness check.

---

## What's new in v3.0

- **Three content-shaped modes** — `portrait` (phone, ~430×844), `horizontal` (video, ~1240×720), `full` (maximized window)
- **`full` now opens a maximized window** — not a new tab
- **Auto-launches Chrome** if not already running
- **Try/retry error handling** — recovers if Chrome is unresponsive
- **Shell wrapper validates modes** — exits code 2 on invalid input
- **macOS Automation permission** note added to troubleshooting

## What was new in v2.0

- **No mode toggle** — Square/Full removed from toolbar. Window size IS the mode. Card is purely responsive (max-width 960px).
- **🪽 Hermes Preview** title with violet accent (#8B5CF6) replaces Square/Full toggle buttons
- **Auto-fit to content** — card shrinks to hug small artifacts (widgets/charts), fills to 960px for full-width layouts
- **Simpler state** — no `state.mode`, no `setMode()`, no body class toggling for modes
- **Backup at** `~/artifact-preview/index.html.backup-v2.1` and `~/artifact-preview/SKILL.md.backup-v2.1`
