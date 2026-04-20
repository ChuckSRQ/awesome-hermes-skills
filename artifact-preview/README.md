<div align="center">

# 🪽 Artifact Preview **v4.2** — Claude Artifacts, But Better 🔥

### Write code. See it live. Instantly. Never lose a version. 🪄

**One-line install • Persistent History • Live Reload • Save as New** ✨

```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash
```

[![macOS](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Chrome](https://img.shields.io/badge/browser-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://google.com/chrome)

[Installation](#-installation-one-line-magic) · [Quick Start](#-quick-start) · [History](#-history--recent-artifacts) · [What's New](#-whats-new-in-v42)

</div>

---

## 🎬 The Pitch

You tell your AI **"build me a fitness dashboard"** → a gorgeous **live, interactive preview** pops open in the perfect Chrome window 📊

Make a change? **Live reload in sub-second** ⚡
Love a version? **Saved to history automatically** 🕐
Want to experiment? Hit **"Save as New"** — your current preview stays safe ✅

**Artifact Preview v4.2** turns raw AI output into a delightful, version-controlled visual experience. Stop losing work. Start building faster. 🔥

---

## 🔥 Key Features

- 🧠 **Smart Auto-Detect** → Portrait 📱 / Horizontal 📺 / Full 🖥️ — chooses the perfect window shape automatically
- ⚡ **Sub-second live reload** with Server-Sent Events — no polling, no lag, just instant ⚡
- ✏️ **Built-in Code Editor** with Code / Split / Preview tabs + `⌘⇧E`
- 📸 **One-click Retina screenshots** → Downloads + Preview.app with Share button
- 🕐 **Recent Artifacts Dropdown** — instantly switch between live and past versions
- 📦 **Persistent History** — automatic timestamped backups (up to 15) with smart readable titles
- ✅ **"Save as New"** — save a variation without touching your live preview
- 🎨 **Modern dark UI** with violet accents, auto-fit smart card, beautiful toast notifications

**Idea → interactive prototype in ~3 seconds.** No hype. That's the actual experience. 🚀

---

## 🆕 What's New in v4.2 ⚡
🌍 Universal Support — Now fully compatible with Windows 🪟 and Linux 🐧. No developer left behind!
🔝 Smart History Sorting — The latest versions now sit right at the top of the dropdown. Intuition achieved! 🚀
📸 Instant Auto-Capture — Whatever is in your artifact.html gets backed up the millisecond the server starts.
🔔 Enhanced Toast Alerts — High-vis "Saved to History" notifications so you know your progress is secure.
➕ The "Save as New" Branch — Experiment without fear! Save a fresh variation without touching your live artifact.
📍 Always-On Pinning — Your "● Current — Live" view is now pinned to the top so you never lose your place.
🛡️ Stability Buffs — Optimized error handling and fixed toast deduplication for a buttery-smooth experience.

---

## 📦 History & Recent Artifacts — Never Lose Work Again 🛟

Every save automatically archives your work with:
- ⏰ Timestamped filename (`20260420-142300-fitness-dashboard.html`)
- 🏷️ Smart title extracted from `<title>` or `<h1>`
- 🔎 One-click access via the toolbar dropdown

**Pro tip:** Hit **"Save as New"** when you love a variation but want to keep building on the live version. Your current artifact stays safe! 💪

---

## 📥 Installation — One-Line Magic ✨

```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash
```

That's it. One command. Installs everything, registers with Hermes, starts the server. 🚀

After install:
```bash
cd ~/artifact-preview && python3 server.py &
bash ~/artifact-preview/open-chrome.sh        # auto mode = pure magic 🪄
```

**Pro tip:** Add this alias to your `~/.zshrc` or `~/.bashrc`:
```bash
alias ap='cd ~/artifact-preview && python3 server.py &'
```

### Uninstall (also one-line):
```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/uninstall.sh | bash
```

---

## 🪟 Launch Modes

| Mode | Size | Best For 🔥 |
|------|------|-------------|
| **Portrait** 📱 | ~430×844 | Phone apps, mobile UI, fitness trackers, Instagram-style |
| **Horizontal** 📺 | ~1240×720 | Dashboards, analytics, data viz, video layouts |
| **Full** 🖥️ | Main display | Websites, landing pages, full applications |

**Auto-detect works automatically** — but you can force a mode:
```bash
bash ~/artifact-preview/open-chrome.sh portrait   # phone window
bash ~/artifact-preview/open-chrome.sh horizontal # video/dashboard
bash ~/artifact-preview/open-chrome.sh full       # maximized
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|:--------:|--------|
| `⌘⇧E` | Toggle HTML editor ✏️ |
| `⌘⇧S` | Save from editor 💾 |
| `⌘⇧R` | Refresh preview 🔄 |

---

## 🎨 Design Standards — Build Beautiful, Not Skeletons 💀

Every artifact should be **complete, polished, and interactive**:

- ✅ **Real functionality** — buttons work, inputs respond, data flows
- ✅ **Modern CSS** — flexbox/grid, CSS variables, smooth transitions, rounded corners
- ✅ **Self-contained** — one HTML file, inline everything, Google Fonts OK
- ✅ **Light-first** — warm white `#F8F7F4` unless content demands dark

### Default Palette 🎨

| | Hex | Use |
|---|-----|-----|
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
├── 🚀 server.py                 # Python HTTP + SSE (background server)
├── 🪟 open-chrome.sh            # Shell wrapper — validates mode, auto-detects
├── 🪟 launcher.py               # Cross-platform launcher (macOS/Windows/Linux)
├── 🍎 open-chrome.applescript   # AppleScript — Chrome window management
├── 📸 share-screenshot.py       # Retina capture → Downloads + Preview.app
├── 🖼️ index.html               # Preview UI + toolbar + Recent dropdown
├── 📝 artifact.html             # Your artifact (overwrite each time)
├── 📂 history/                 # Auto-backup of all past artifacts
└── 📄 artifacts.json            # History manifest
```

---

## ⚙️ Requirements

| | |
|---|---|
| 🍎 **macOS 12+** | AppleScript window management |
| 🌐 **Google Chrome** | Target browser |
| 🐍 **Python 3.8+** | HTTP server with SSE |
| 🔐 **Automation permissions** | One-time: System Settings → Privacy & Security → Automation → grant Terminal → Chrome |

### Windows 🪟 & Linux 🐧
Optional (for precise window sizing):
```bash
pip install screeninfo pywinctl
```

---

## 🔧 Server Commands

```bash
# Start server
cd ~/artifact-preview && python3 server.py &

# Stop server
lsof -ti :8765 | xargs kill 2>/dev/null || true

# Verify running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 ✅

# Port is 8765. Override: export ARTIFACT_PREVIEW_PORT=9000
```

---

## 🚀 Quick Start

```bash
# 1. Install (one line!)
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash

# 2. Start the server
cd ~/artifact-preview && python3 server.py &

# 3. Generate → save → preview (your agent does this)
cd ~/artifact-preview
cat > artifact.html << 'ENDOFHTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Cool App</title>
</head>
<body>
    <!-- your content -->
</body>
</html>
ENDOFHTML

# Triggers save + archive + toast + live reload ⚡
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null

# 4. Open the preview — auto mode is pure magic 🪄
bash ~/artifact-preview/open-chrome.sh
```

---

<div align="center">

### Built for [Hermes Agent](https://github.com/ChuckSRQ/awesome-hermes-skills) 🔥

*Part of [Awesome Hermes Skills](https://github.com/ChuckSRQ/awesome-hermes-skills) — production-ready AI agent skills.*

**⭐ Star the repo if this saved you time.**

</div>
