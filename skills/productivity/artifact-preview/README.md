<div align="center">

# 🪽 Artifact Preview v3.0

### **Write code. See it live. Instantly.**

*The "Claude Artifacts" experience — for any AI agent.*

[![macOS](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Chrome](https://img.shields.io/badge/browser-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://google.com/chrome)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)

[Installation](#-installation) · [Quick Start](#-quick-start) · [Modes](#-launch-modes) · [Features](#-features)

</div>

---

## 🎬 The Pitch

You're working with an AI agent. You say *"build me a dashboard"* — and you get... a wall of code you have to copy, paste, save, and open. Every. Single. Time.

**Artifact Preview kills that loop.**

Your agent writes HTML/CSS/JS → the browser opens **automatically** → you see a polished, live, interactive preview. Update the code? It reloads in real-time. No refresh buttons. No manual steps. No friction.

> 💡 **One file. Zero config. Instant preview.**

---

## ✨ The Magic Trick

🧠 **Auto-detect mode** — just write your HTML. The launcher reads your artifact and picks the right window size. Phone app? Portrait. Dashboard? Horizontal. Full website? Maximized. No arguments needed.

🖥️ **Three content-shaped windows** — not one-size-fits-all tabs. Portrait for mobile artboards (~430×844), horizontal for dashboards (~1240×720), full for complete websites (fills your primary display).

📐 **Smart card that hugs your content** — small widgets get a compact centered card. Full-width websites expand edge-to-edge. The preview adapts to what you built, not the other way around.

⚡ **Sub-second live reload** — save your code and watch it update instantly via Server-Sent Events. No polling. No delay. No refresh button.

✏️ **Built-in code editor** — Code / Split / Preview tabs. Edit HTML inline, save, see changes. `Cmd+Shift+E` to toggle.

📸 **One-click screenshot + share** — captures at Retina resolution, opens in macOS Preview with the full system share sheet. AirDrop, Messages, Mail — whatever.

---

## 🔥 The Workflow

```
You: "Build me a fitness app dashboard"

   AI agent writes HTML/CSS/JS
          ↓
   Saves to ~/artifact-preview/artifact.html
          ↓
   Chrome opens automatically in portrait mode
          ↓
   You see a live, polished, interactive app
          ↓
   "Add a heart rate widget"
          ↓
   Agent updates the file → live reload → instant update
```

**Total time from idea to preview: ~3 seconds.**

---

## 📦 Installation

```bash
# Clone or copy the skill
mkdir -p ~/artifact-preview
cp skills/productivity/artifact-preview/*.sh ~/artifact-preview/
cp skills/productivity/artifact-preview/*.applescript ~/artifact-preview/
cp skills/productivity/artifact-preview/server.py ~/artifact-preview/
cp skills/productivity/artifact-preview/index.html ~/artifact-preview/
chmod +x ~/artifact-preview/open-chrome.sh

# Start the server (one time, runs in background)
cd ~/artifact-preview && python3 server.py &
```

> 🍎 **macOS only** — requires macOS 12+ (Monterey) and Google Chrome. First run will prompt for Automation permissions (System Preferences → Privacy & Security → Automation → grant to Terminal).

---

## 🚀 Quick Start

### Auto mode (recommended)

```bash
# Just launch — it detects the right window size from your content
bash ~/artifact-preview/open-chrome.sh
```

That's it. Add a `<meta name="preview-mode" content="portrait">` tag to your HTML for explicit control, or let the heuristics figure it out.

### Explicit modes

```bash
bash ~/artifact-preview/open-chrome.sh portrait    # 📱 phone-sized window
bash ~/artifact-preview/open-chrome.sh horizontal  # 📺 wide window
bash ~/artifact-preview/open-chrome.sh full        # 🖥️ maximized
```

---

## 🪟 Launch Modes

| Mode | Size | Emoji | Best For |
|------|------|:-----:|----------|
| **Portrait** | ~430×844 | 📱 | Phone apps, mobile UI, Instagram-style, fitness apps |
| **Horizontal** | ~1240×720 | 📺 | Dashboards, analytics, video layouts, data viz |
| **Full** | Main display | 🖥️ | Websites, landing pages, full applications |

### How auto-detect works

1. **Meta tag** — `<meta name="preview-mode" content="portrait|horizontal|full">` (explicit, always wins)
2. **Heuristic** — finds `<nav>`/`<footer>` → full, mobile viewport + narrow layout → portrait
3. **Default** — horizontal (good middle ground)

---

## 🎯 Features

| Feature | Details |
|---------|---------|
| 🧠 **Auto-detect** | Reads your HTML to pick the right window mode |
| 🖥️ **Three modes** | Portrait, horizontal, full — content-shaped windows |
| ⚡ **Live reload** | SSE pushes updates instantly, zero latency |
| 📐 **Smart card** | Hugs small widgets, fills for full websites |
| ✏️ **Inline editor** | Code / Split / Preview with keyboard shortcuts |
| 📸 **Screenshot** | Retina capture → macOS Preview → system share |
| 🎨 **Design system** | Instrument Sans, violet accent, modern CSS |
| 🔌 **Zero deps** | One HTML file, no npm, no build step |
| 🧹 **Clean launch** | No profile picker, no blank tabs, no Chrome drama |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|:--------:|--------|
| `⌘⇧E` | Toggle HTML editor |
| `⌘⇧S` | Save from editor |
| `⌘⇧R` | Refresh preview |

---

## 🎨 Design Standards

Every artifact should be **complete, beautiful, and interactive** — not a skeleton.

- **Real functionality** — buttons work, inputs respond, data flows
- **Modern CSS** — flexbox/grid, CSS variables, smooth transitions, rounded corners
- **Self-contained** — one HTML file, inline everything, Google Fonts OK
- **Light-first** — warm white backgrounds (`#F8F7F4`) unless content demands dark

### Default palette

| Color | Hex | Usage |
|-------|-----|-------|
| ⬜ Warm white | `#F8F7F4` | Background |
| 🟪 Violet | `#8B5CF6` | Primary accent |
| ⬛ Near-black | `#1A1A2E` | Text |
| 🟩 Green | `#22C55E` | Success |
| 🟥 Red | `#EF4444` | Error |

Font: **Instrument Sans** via Google Fonts.

---

## 📁 Architecture

```
~/artifact-preview/
├── 🚀 server.py              # Python HTTP + SSE (background process)
├── 🪟 open-chrome.sh         # Shell wrapper — validates mode, auto-detects
├── 🍎 open-chrome.applescript # AppleScript — Chrome window management
├── 📸 share-screenshot.py    # Retina capture → Preview.app
├── 🖼️ index.html             # Preview UI + toolbar (don't edit)
├── 📝 artifact.html          # Your artifact (overwrite each time)
└── 📂 history/               # Auto-backup of past artifacts
```

---

## ⚙️ Requirements

| Requirement | Why |
|-------------|-----|
| 🍎 **macOS 12+** | AppleScript window management, `NSScreen` API |
| 🌐 **Google Chrome** | Target browser for preview windows |
| 🐍 **Python 3.8+** | HTTP server with Server-Sent Events |
| 🔐 **Automation permissions** | Terminal needs access to control Chrome |

---

## 🔧 Configuration

Everything lives in `~/artifact-preview/`. Server runs on port `8765`. Change it in `server.py` if needed.

```bash
# Start server
cd ~/artifact-preview && python3 server.py &

# Stop server
pkill -f "artifact-preview/server.py"

# Verify it's running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200
```

---

<div align="center">

### Built for [Hermes Agent](https://github.com/ChuckSRQ/awesome-hermes-skills)

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — a curated collection of production-ready AI agent skills.*

**⭐ Star the repo if this saved you time.**

</div>
