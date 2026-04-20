<div align="center">

# 🪽 Artifact Preview v4.0

### **Write code. See it live. Instantly. 🔥**

*The "Claude Artifacts" experience — for any AI agent.*

[![macOS](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Linux](https://img.shields.io/badge/platform-Linux-CC0000?logo=linux&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Chrome](https://img.shields.io/badge/browser-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://google.com/chrome)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)

[Installation](#-installation) · [Quick Start](#-quick-start) · [Modes](#-launch-modes) · [Features](#-features)

</div>

---

🎬 The Pitch
You you're working with an AI agent. You say "build me a dashboard" and you get... a wall of code you have to copy, paste, save, and open. Every. Single. Time. 😩

Artifact Preview kills that loop dead. 💀🔥

Your agent writes HTML/CSS/JS → the browser opens automatically 🚀 → you see a polished, live, interactive preview. Update the code? It reloads in real-time. No refresh buttons. No manual steps. Zero friction. ⚡

💡 One file. Zero config. Instant preview. 🌈

🔥 Key Features
🧠 Auto-Detect Mode
It reads your code and intuitively picks the right window. Coding a mobile app? You get Portrait 📱. A complex dashboard? Horizontal 📺. A full website? Maximized 🖥️. No configuration needed!

🖥️ Three Content-Shaped Windows
Stop using one-size-fits-all tabs! Choose from Portrait (~430×844), Horizontal (~1240×720), or Full Display. It fits your content perfectly. 📐

📐 Smart Card UI
Small widgets get a compact, centered card 💎. Full-width websites expand edge-to-edge 🌊. The frame intelligently adapts to whatever you've built. ✨

⚡ Sub-Second Live Reload
Save your code and watch the magic happen instantly via Server-Sent Events. No polling, no delay, and zero refresh buttons. 🌬️

✏️ Built-in Code Editor
Effortlessly toggle between Code, Split, or Preview tabs. Edit your HTML inline and see changes immediately with a simple Cmd+Shift+E. ⌨️

📸 One-Click Screenshot + Share
Grab a high-res Retina capture 📸 that sends directly to macOS Preview or your system share sheet. AirDrop, Message, or Mail your work in a heartbeat! 🕊️

🎨 Modern Design System
Featuring Instrument Sans, vibrant violet accents, and warm white backgrounds. Every artifact looks like a premium product right out of the box. ✨

🔌 Zero Dependencies
A single, lightweight HTML file. No npm, no complex build steps, and no messy config files. It just works. 🔌✨

🧹 Clean Chrome Launch
No profile pickers, no annoying blank tabs, and zero Chrome drama. It opens a dedicated window and stays out of your way. 🧼

🍎 Proper macOS Integration
Uses Swift (NSScreen.main) for perfect logical screen sizing and AppleScript for precise window bounds. No dual-monitor bleed. 🎯

🕐 **Recent Artifacts Dropdown**
Instantly switch between current and previous previews without losing work. New generations never overwrite old ones. A clean "Recent" dropdown in the toolbar gives you access to the last ~15 artifacts.

📦 **Persistent History**
Automatic readable backups with one-click access. Every artifact is archived with a timestamp and readable title.

🪟 **Cross-Platform Ready**
macOS unchanged; foundation added for Windows + Linux (launcher.py + screeninfo/PyWinCtl).

---

## 🆕 What's New in v4.0 🚀

🕐 **Recent Artifacts Dropdown**
A clean "Recent" dropdown appears automatically in the toolbar. Every new artifact generation becomes the live preview; the previous one moves into the dropdown — fully accessible and editable.

📦 **Persistent History**
Automatic readable backups stored in `history/` with timestamped filenames (e.g., `20260418-232400-dashboard.html`). Never lose an artifact again.

🪟 **Cross-Platform Launcher**
New `launcher.py` unifies Chrome launching across macOS, Windows, and Linux. macOS users see zero change; Windows/Linux users get proper window sizing and positioning.

---

## 🔥 The Workflow

```
You: "Build me a fitness app dashboard"

   AI agent writes HTML/CSS/JS
          ↓
   Saves to ~/artifact-preview/artifact.html
          ↓
   Chrome opens automatically in portrait mode 📱
          ↓
   You see a live, polished, interactive app ✨
          ↓
   "Add a heart rate widget"
          ↓
   Agent updates the file → live reload → instant update ⚡
```

**Total time from idea to preview: ~3 seconds. 🚀**

---

## 📦 Installation

```bash
# Clone or copy the skill
mkdir -p ~/artifact-preview
cp skills/productivity/artifact-preview/*.sh ~/artifact-preview/
cp skills/productivity/artifact-preview/*.applescript ~/artifact-preview/
cp skills/productivity/artifact-preview/server.py ~/artifact-preview/
cp skills/productivity/artifact-preview/index.html ~/artifact-preview/
cp skills/productivity/artifact-preview/launcher.py ~/artifact-preview/
chmod +x ~/artifact-preview/open-chrome.sh
chmod +x ~/artifact-preview/launcher.py

# Start the server (one time, runs in background)
cd ~/artifact-preview && python3 server.py &
```

### macOS 🍎
> Requires macOS 12+ (Monterey) and Google Chrome. First run will prompt for Automation permissions (System Preferences → Privacy & Security → Automation → grant to Terminal).

### Windows 🪟 & Linux 🐧
> For precise window control, install optional dependencies:
> ```bash
> pip install screeninfo pywinctl
> ```
> The launcher works without them using basic window management.

---

## 🚀 Quick Start

### Auto mode (recommended) ⚡

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

### Using the Recent Dropdown 🕐

The dropdown appears automatically in the toolbar:
- **Top item**: "Current — Live" (the active `artifact.html`)
- **Below**: last artifacts like "Mobile Login — 3m ago" or "Dashboard — Apr 18"
- Click any entry to load it into the preview
- Edit it inline and save — changes are preserved

---

## 🪟 Launch Modes

| Mode | Size | Emoji | Best For 🔥 |
|------|------|:-----:|-------------|
| **Portrait** | ~430×844 | 📱 | Phone apps, mobile UI, Instagram-style, fitness apps |
| **Horizontal** | ~1240×720 | 📺 | Dashboards, analytics, video layouts, data viz |
| **Full** | Main display | 🖥️ | Websites, landing pages, full applications |

### How auto-detect works 🧠

1. **Meta tag** — `<meta name="preview-mode" content="portrait|horizontal|full">` (explicit, always wins)
2. **Heuristic** — finds `<nav>`/`<footer>` → full, mobile viewport + narrow layout → portrait
3. **Default** — horizontal (good middle ground)

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|:--------:|--------|
| `⌘⇧E` | Toggle HTML editor ✏️ |
| `⌘⇧S` | Save from editor 💾 |
| `⌘⇧R` | Refresh preview 🔄 |

---

## 🎨 Design Standards

Every artifact should be **complete, beautiful, and interactive** — not a skeleton 💀

- **Real functionality** — buttons work, inputs respond, data flows
- **Modern CSS** — flexbox/grid, CSS variables, smooth transitions, rounded corners
- **Self-contained** — one HTML file, inline everything, Google Fonts OK
- **Light-first** — warm white backgrounds (`#F8F7F4`) unless content demands dark

### Default palette 🎨

| Color | Hex | Usage |
|-------|-----|-------|
| ⬜ Warm white | `#F8F7F4` | Background |
| 🟪 Violet | `#8B5CF6` | Primary accent |
| ⬛ Near-black | `#1A1A2E` | Text |
| 🟩 Green | `#22C55E` | Success ✅ |
| 🟥 Red | `#EF4444` | Error ❌ |

Font: **Instrument Sans** via Google Fonts.

---

## 📁 Architecture

```
~/artifact-preview/
├── 🚀 server.py              # Python HTTP + SSE (background process)
├── 🪟 open-chrome.sh         # Shell wrapper — validates mode, auto-detects (macOS)
├── 🪟 launcher.py            # Cross-platform launcher (macOS/Windows/Linux)
├── 🍎 open-chrome.applescript # AppleScript — Chrome window management (macOS)
├── 📸 share-screenshot.py    # Retina capture → Preview.app
├── 🖼️ index.html             # Preview UI + toolbar + Recent dropdown
├── 📝 artifact.html          # Your artifact (overwrite each time)
├── 📂 history/               # Auto-backup of past artifacts
└── 📄 artifacts.json         # History manifest
```

---

## ⚙️ Requirements

| Requirement | Why |
|-------------|-----|
| 🍎 **macOS 12+** | AppleScript window management, `NSScreen` API |
| 🪟 **Windows 10+** | Chrome + optional PyWinCtl for window control |
| 🐧 **Linux** | Chrome + optional PyWinCtl/wmctrl for window control |
| 🌐 **Google Chrome** | Target browser for preview windows |
| 🐍 **Python 3.8+** | HTTP server with Server-Sent Events |
| 🔐 **Automation permissions** | Terminal needs access to control Chrome (macOS) |

### Optional Dependencies (Windows/Linux)

```bash
pip install screeninfo pywinctl
```

These enable precise window positioning and sizing. The launcher works without them using basic browser APIs.

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
# → 200 ✅
```

---

<div align="center">

### Built for [Hermes Agent](https://github.com/ChuckSRQ/awesome-hermes-skills) 🔥

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — a curated collection of production-ready AI agent skills.*

**⭐ Star the repo if this saved you time.**

</div>
