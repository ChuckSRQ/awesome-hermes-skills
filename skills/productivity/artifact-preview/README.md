# 🪽 Artifact Preview v3.0

> *The "Claude Artifacts" experience — for any AI agent. Write code, see it live. Instantly.*

**🍎 macOS only** — Requires macOS 12+ and Google Chrome. Uses AppleScript for window management and macOS-native APIs for screen detection.

---

## Download / Install

```bash
# Copy to your artifact-preview directory
mkdir -p ~/artifact-preview
cp skills/productivity/artifact-preview/open-chrome.sh ~/artifact-preview/
cp skills/productivity/artifact-preview/open-chrome.applescript ~/artifact-preview/
cp skills/productivity/artifact-preview/server.py ~/artifact-preview/
cp skills/productivity/artifact-preview/index.html ~/artifact-preview/
chmod +x ~/artifact-preview/open-chrome.sh
```

---

## What is this?

Write a prompt. Get a **real, working app** — not a skeleton, not a toy. A polished, interactive artifact that opens live in a Chrome window the moment it's generated. Three window modes for different content types. Edit inline. Screenshot it. Share it. All in seconds.

**Perfect for:** dashboards, UI components, prototypes, interactive demos, forms, games, data visualizations, landing pages, charts, plugins

```
make a dashboard showing my team stats
build a landing page with a contact form
show me an interactive map component
create a tic-tac-toe game
```

---

## ✨ What's new in v3.0

- 🪽 **Three launch modes** — Portrait (phone artboards), Horizontal (video/landscape), Full (maximized to main display)
- 📐 **Smart screen detection** — uses `NSScreen.main` to fill the primary display without bleeding into external monitors
- 🚀 **Clean Chrome launch** — no profile picker, no blank tabs, opens directly with content
- ✏️ **Inline HTML editor** — Code / Split / Preview tabs right in the toolbar
- 📸 **Screenshot + macOS Share** — one click captures to Preview.app with the full system share sheet
- ⚡ **Zero-latency reload** — SSE pushes updates the instant you save

---

## 🎯 Core features

- 🏗️ **Self-contained HTML** — one file, no build step, no npm, no dependencies (except Google Fonts)
- 🎨 **Modern design** — Instrument Sans, violet accent (#8B5CF6), clean typography
- 🖥️ **Three window modes** — Portrait (~430×844), Horizontal (~1240×720), Full (main display)
- ⌨️ **Keyboard-first** — `Cmd+Shift+E` editor, `Cmd+Shift+S` save, `Cmd+Shift+R` refresh
- 📦 **Drop-in setup** — Python HTTP server with SSE, one command to start, zero config

---

## 🚀 Quick Start

### One-time setup

```bash
mkdir -p ~/artifact-preview
chmod +x ~/artifact-preview/open-chrome.sh
```

Start the server:
```bash
cd ~/artifact-preview && python3 server.py &
```

### Launch preview

```bash
# Phone/mobile content → portrait window
bash ~/artifact-preview/open-chrome.sh portrait

# Video/landscape content → horizontal window
bash ~/artifact-preview/open-chrome.sh horizontal

# Full website → maximized window
bash ~/artifact-preview/open-chrome.sh full
```

---

## 🪟 Launch Modes

| Mode | Command | Window Size | Best For |
|------|---------|-------------|----------|
| **Portrait** | `bash ~/artifact-preview/open-chrome.sh portrait` | ~430×844 | Phone apps, mobile UI, Instagram-style |
| **Horizontal** | `bash ~/artifact-preview/open-chrome.sh horizontal` | ~1240×720 | Dashboards, video, wide layouts |
| **Full** | `bash ~/artifact-preview/open-chrome.sh full` | Main display | Websites, landing pages, full apps |

---

## 📁 File Structure

```
~/artifact-preview/
├── server.py              # Python HTTP server with SSE live reload
├── open-chrome.sh         # Shell wrapper (validates mode, calls AppleScript)
├── open-chrome.applescript # macOS AppleScript — Chrome window management
├── share-screenshot.py    # Screenshot to macOS Preview + Share
├── index.html             # Preview UI with toolbar (don't edit)
├── artifact.html          # Your generated artifact (overwrite each time)
└── history/               # Backup of past artifacts
```

---

## 🎨 Design Standards

Artifacts should be **complete, beautiful, and interactive**:

- **Not a skeleton** — real working UI with real functionality
- **Modern CSS** — Flexbox/grid, CSS variables, smooth transitions
- **Interactive** — buttons work, inputs accept text, animations play
- **Self-contained** — one HTML file, no external deps (except Google Fonts)
- **Light-first** — default to white/warm backgrounds unless content demands dark

### Default palette

| Element | Value |
|---------|-------|
| Background | `#F8F7F4` (warm white) |
| Surface | `#F0EEF6` (light lavender) |
| Text | `#1A1A2E` (near-black) |
| Primary accent | `#8B5CF6` (violet) |
| Success | `#22C55E` |
| Error | `#EF4444` |
| Radius | 12px cards, 8px buttons |
| Font | Instrument Sans |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+E` | Toggle HTML editor |
| `Cmd+Shift+S` | Save from editor |
| `Cmd+Shift+R` | Refresh preview |

---

## ⚙️ Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | macOS 12+ (Monterey or later) |
| **Browser** | Google Chrome |
| **Python** | 3.8+ |
| **Permissions** | Terminal needs Automation access to control Chrome (System Preferences → Privacy & Security → Automation) |

---

## 🔧 Configuration

| Setting | Default | Notes |
|---------|---------|-------|
| Artifact directory | `~/artifact-preview/` | Configurable |
| HTTP server port | `8765` | In server.py |
| Preview URL | `http://localhost:8765` | — |

---

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — a curated collection of production-ready skills for Hermes Agent.*
