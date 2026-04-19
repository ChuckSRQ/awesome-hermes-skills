<div align="center">

# 🪽 Artifact Preview v4.0

### **Write code. See it live. Instantly. 🔥**

*The "Claude Artifacts" experience — for any AI agent.*

[![macOS](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Chrome](https://img.shields.io/badge/browser-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://google.com/chrome)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)

[Installation](#-installation) · [Quick Start](#-quick-start) · [Modes](#-launch-modes) · [Features](#-features)

</div>

---

🎬 The Pitch
You’re working with an AI agent. You say "build me a dashboard" and you get... a wall of code you have to copy, paste, save, and open. Every. Single. Time. 😩

Artifact Preview kills that loop dead. 💀🔥

Your agent writes HTML/CSS/JS → the browser opens automatically 🚀 → you see a polished, live, interactive preview. Update the code? It reloads in real-time. No refresh buttons. No manual steps. Zero friction. ⚡

💡 One file. Zero config. Instant preview. 🌈

🔥 Key Features
🧠 Auto-Detect Mode
It reads your code and intuitively picks the right window. Coding a mobile app? You get Portrait 📱. A complex dashboard? Horizontal 📺. A full website? Maximized 🖥️. No configuration needed!

🖥️ Three Content-Shaped Windows
Stop using one-size-fits-all tabs! Choose from Portrait (~430×844), Horizontal (~1240×720), or Full Display. It fits your content perfectly. 📐

📐 Smart Card UI
Small widgets get a compact, centered card 💎. Full-width websites expand edge-to-edge 🌊. The frame intelligently adapts to whatever you’ve built.

⚡ Sub-Second Live Reload
Save your code and watch the magic happen instantly via Server-Sent Events. No polling, no delay, and zero refresh buttons. 🌬️

✏️ Built-in Code Editor
Effortlessly toggle between Code, Split, or Preview tabs. Edit your HTML inline and see changes immediately with a simple Cmd+Shift+E. ⌨️

📸 One-Click Screenshot + Share
Grab a high-res Retina capture 📸 that sends directly to macOS Preview or your system share sheet. AirDrop, Message, or Mail your work in a heartbeat! 🕊️

🎨 Modern Design System
Featuring Instrument Sans, vibrant violet accents, and warm white backgrounds. Every artifact looks like a premium product right out of the box. ✨

🔍 Recent Artifacts Dropdown
Instantly switch between current and previous previews without losing work. New generations never overwrite old ones — a clean dropdown in the toolbar gives one-click access to your history. 📜

💾 Persistent History
Automatic readable backups with timestamped names. Every artifact is safely archived and accessible from the dropdown — no more lost previews. 🗂️

🔄 Cross-Platform Ready
macOS unchanged with full polish. Foundation added for Windows and Linux via `launcher.py` with `screeninfo` and `PyWinCtl` support. 🖥️

🔌 Zero Dependencies
A single, lightweight HTML file. No npm, no complex build steps, and no messy config files. It just works. 🔌✨

🧹 Clean Chrome Launch
No profile pickers, no annoying blank tabs, and zero Chrome drama. It opens a dedicated window and stays out of your way. 🧼

🍎 Proper macOS Integration
Uses Swift (NSScreen.main) for perfect logical screen sizing and AppleScript for precise window bounds. No dual-monitor bleed. 🎯

## 🆕 What's New in v4.0 🚀
Artifact Preview v4.0 adds persistent history and cross-platform support while keeping the elegant simplicity you love. 💥

📜 **Recent Artifacts Dropdown:** A clean "Recent" menu in the toolbar gives instant access to the last ~10 previews. New AI content becomes live; the previous version moves to the dropdown — never lose work again.

🗂️ **Persistent History:** Every artifact is automatically archived with readable timestamped names. Click any past version to load it back into the preview.

⚡ **Sub-Second Performance:** All v3 performance characteristics preserved — same SSE live reload, same instant updates.

🖥️ **Cross-Platform Foundation:** macOS unchanged. Windows and Linux support added via `launcher.py` with optional `screeninfo` and `PyWinCtl` libraries.

---

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
# Run the install script
bash ~/artifact-preview/install.sh

# Start the server (one time, runs in background)
cd ~/artifact-preview && python3 server.py &
```

> 🍎 **macOS** — requires macOS 12+ and Google Chrome. First run prompts for Automation permissions (System Preferences → Privacy & Security → Automation → grant to Terminal).
>
> 🪟 **Windows / 🐧 Linux** — also run: `pip install screeninfo pywinctl`

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
├── 🪟 open-chrome.sh         # Shell wrapper — validates mode, auto-detects
├── 🍎 open-chrome.applescript # AppleScript — Chrome window management
├── 📸 share-screenshot.py    # Retina capture → Preview.app
├── 🖼️ index.html             # Preview UI + toolbar (don't edit)
├── 📝 artifact.html          # Your artifact (overwrite each time)
└── 📂 history/               # Auto-backup of past artifacts
```

---

## ⚙️ Requirements

|| Requirement | Why |
||-------------|-----|
|| 🍎 **macOS 12+** | AppleScript window management, `NSScreen` API |
|| 🪟 **Windows / 🐧 Linux** | `pip install screeninfo pywinctl` for window control |
|| 🌐 **Google Chrome** | Target browser for preview windows |
|| 🐍 **Python 3.8+** | HTTP server with Server-Sent Events |
|| 🔐 **Automation permissions** | Terminal needs access to control Chrome |

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
