# 🔥🪽 Artifact Preview v2.0

> *The "Claude Artifacts" experience — for any AI agent. Write code, see it live. Instantly.*

---

## Download / Install

```bash
# Copy to your skills directory
cp -r ~/.hermes/skills/awesome-hermes-skills/productivity/artifact-preview ~/.hermes/skills/
```

---

## What is this?

Write a prompt. Get a **real, working app** — not a skeleton, not a toy. A polished, interactive artifact that opens live in a compact browser window the moment it's generated. Edit it inline. Screenshot it. Share it. All in seconds.

**Perfect for:** dashboards, UI components, prototypes, interactive demos, forms, games, data visualizations, landing pages, charts, plugins

```
make a dashboard showing my team stats
build a landing page with a contact form
show me an interactive map component
create a tic-tac-toe game
```

---

## ✨ What's new in v2.0

- 🪽 **Hermes Preview** — branded compact window with violet accents. No mode clutter, no toggles. Just preview.
- 📐 **Auto-fit smart card** — the preview *shrinks to hug* small widgets and charts, *expands* for full-width websites. No manual resizing. It just knows.
- ✏️ **Inline HTML editor** — Code / Split / Preview tabs right in the toolbar. Edit live, see changes in real-time.
- 📸 **Screenshot + macOS Share** — one click captures to Preview.app with the full system share sheet. AirDrop, Messages, Mail — whatever.
- ⚡ **Zero-latency reload** — SSE pushes updates the instant you save. No polling, no waiting, no refresh buttons.

---

## 🎯 Core features

- 🏗️ **Self-contained HTML** — one file, no build step, no npm, no dependencies (except Google Fonts)
- 🎨 **Modern dark theme** — midnight blue + violet accent (#8B5CF6), glassmorphism card, clean typography
- 🖥️ **Smart windowing** — compact 640px window for widgets, full browser tab for websites. You pick at launch.
- ⌨️ **Keyboard-first** — `Cmd+Shift+E` editor, `Cmd+Shift+S` save, `Cmd+Shift+R` refresh
- 📦 **Drop-in setup** — Python server, one command to start, zero config

---

## 🚀 Quick Start

### One-time setup

```bash
mkdir -p ~/artifact-preview
cd ~/artifact-preview
python3 -m http.server 8765 &
```

To verify it's running:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# Should return 200
```

### Open the preview window

```bash
osascript ~/artifact-preview/open-chrome.sh
```

This opens Chrome at 1/4 screen size (top-left). The window position and size are customizable in `open-chrome.sh`.

---

## 📁 File Structure

```
~/artifact-preview/
├── index.html          # Your artifact — single self-contained HTML file
├── open-chrome.sh     # macOS script to open compact preview window
└── history/            # Saved artifacts (when no Obsidian vault)
    └── YYYY-MM-DD-slugified-title.html
```

---

## 🎨 Design Standards

Artifacts should be **complete, beautiful, and interactive**:

- **Not a skeleton** — real working UI with real functionality
- **Modern CSS** — good typography, nice colors, smooth animations
- **Interactive** — buttons work, inputs accept text, animations play
- **Self-contained** — one HTML file, no external deps (except Google Fonts)
- **Responsive** — works on laptop screens, not just desktop

### Default palette

| Element | Value |
|---------|-------|
| Background (dark) | `#0f172a` |
| Background (light) | `#f8fafc` |
| Primary accent | `#6366f1` (indigo) or `#8B5CF6` (violet) |
| Cards | Semi-transparent + `backdrop-filter: blur` |
| Font | system-ui or Inter from Google Fonts |
| Style | Rounded corners, subtle shadows, smooth transitions |

---

## 🔄 Workflow

1. **Generate** → Write complete HTML/CSS/JS to `index.html`
2. **Save** → Artifact saved to Obsidian vault (if configured) or `history/`
3. **Open** → Preview window opens automatically
4. **Confirm** → Tell user it's ready
5. **Update** → On changes, overwrite `index.html` + re-save

---

## ⚙️ Server Management

Restart if needed:
```bash
pkill -f "http.server 8765"
cd ~/artifact-preview && python3 -m http.server 8765 &
```

---

## 📦 Artifact Storage

**With Obsidian:**
- Artifact HTML: `<vault>/03-Notes/artifacts/YYYY-MM-DD-slugified-title.html`
- Artifact index: `<vault>/03-Notes/artifacts/YYYY-MM-DD-slugified-title.md`

**Without Obsidian (fallback):**
- Artifact HTML: `<artifact-preview-dir>/history/YYYY-MM-DD-slugified-title.html`

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+E` | Open editor |
| `Cmd+Shift+S` | Save |
| `Cmd+Shift+R` | Refresh preview |

---

## 🔧 Configuration

| Setting | Default | Notes |
|---------|---------|-------|
| Artifact directory | `~/artifact-preview/` | Configurable |
| HTTP server port | `8765` | Configurable |
| Preview URL | `http://localhost:8765` | — |
| Window size (widget) | 640px wide | Compact mode |
| Window size (website) | Full browser tab | Wide mode |

---

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — a curated collection of production-ready skills for Hermes Agent.*
