<div align="center">

# 🪽 Artifact Preview **v4.2**

### **Write code. See it live. Instantly. Never lose a version.**

*The ultimate live HTML/CSS/JS preview for any AI agent — now with smart persistent history that actually works.*

[![macOS](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Linux](https://img.shields.io/badge/platform-Linux-CC0000?logo=linux&logoColor=white)](https://github.com/ChuckSRQ/awesome-hermes-skills)
[![Chrome](https://img.shields.io/badge/browser-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://google.com/chrome)

[Installation](#-installation) · [Quick Start](#-quick-start) · [History \& Versions](#-history--recent-artifacts) · [What's New in v4.2](#-whats-new-in-v42)

</div>

---

🎬 **The Pitch**
Tired of generating beautiful HTML only to watch it vanish the moment you create the next one? 😩

**Artifact Preview v4.2** fixes that forever.

Tell your agent "build me a fitness dashboard" → polished interactive preview opens instantly 📊 → make changes → **live reload in sub-seconds** ⚡ → and **every version is automatically saved to history** with one-click access.

No more "where did that cool version go?" moments. Ever.

---

🔥 **Key Features**

- 🧠 **Smart Auto-Detect** → chooses Portrait 📱, Horizontal 📺 or Full 🖥️ based on your content
- ⚡ **Sub-second live reload** with Server-Sent Events (no polling!)
- ✏️ **Built-in Code Editor** with Code / Split / Preview tabs + keyboard shortcuts
- 📸 **One-click Retina screenshots** → saves to Downloads + opens Preview with Share button
- 🕐 **Recent Artifacts Dropdown** — instantly switch between live and past versions
- 📦 **Persistent History** — automatic timestamped backups (up to 15) with readable titles
- ✅ **"Save as New" button** — add the current editor state to history **without touching your live preview**
- 🪟 **Cross-platform launcher** (macOS native + solid Windows/Linux support)
- 🎨 Modern dark-first UI with Instrument Sans, violet accents, and auto-fit smart card

**Idea → interactive prototype in ~3 seconds.** That's not hype. That's the experience.

---

### 🆕 What's New in **v4.2** 🔥

- **Newest versions now appear at the top** of the Recent dropdown (finally intuitive!)
- **Auto-capture on server startup** — whatever is in `artifact.html` gets saved to history automatically
- **Beautiful "Saved to history" toasts** — you'll actually *see* when your work is safely backed up
- **"Save as New" button** in the editor — save the current editor state as a brand-new history entry without overwriting your live artifact
- **Pinned "● Current — Live"** entry in the dropdown so you always know what you're looking at
- Fixed toast deduplication and better error handling

History is no longer an afterthought — it's now a **delightful, reliable superpower**.

---

### 📦 **History & Recent Artifacts** — Never Lose Work Again

Every time you save (normal Save or **Save as New**), the artifact is automatically archived with:
- Timestamped filename (`20260420-142300-fitness-dashboard.html`)
- Extracted title from `<title>` or `<h1>`
- One-click access via the toolbar dropdown

**Pro tip**: Use the **Save as New** button when you love a variation but want to keep experimenting on the live version.

---

## 🔥 The Workflow

```
You: "Build me a fitness app dashboard"

   AI agent writes HTML/CSS/JS
          ↓
   Saves to ~/artifact-preview/artifact.html
          ↓
   curl POST triggers save + archive + toast + live reload
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

```bash
# 1. Start the server (do this once)
cd ~/artifact-preview && python3 server.py &

# 2. Generate → save → preview (your agent should do this)
cd ~/artifact-preview
cat > artifact.html << 'ENDOFHTML'
[your full HTML here]
ENDOFHTML

curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null

# 3. Open the preview
bash ~/artifact-preview/open-chrome.sh   # auto mode = magic
```

The Recent dropdown and toasts will guide you from there.

### Using the Recent Dropdown 🕐

The dropdown appears automatically in the toolbar:
- **Top item**: "● Current — Live" (the active `artifact.html`)
- **Below**: past artifacts like "Mobile Login — 3m ago" or "Dashboard — Apr 20"
- Click any entry to load it into the preview
- **Save as New** in the editor → save a variation without overwriting the live artifact

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
├── 🪟 launcher.py             # Cross-platform launcher (macOS/Windows/Linux)
├── 🍎 open-chrome.applescript  # AppleScript — Chrome window management (macOS)
├── 📸 share-screenshot.py     # Retina capture → Preview.app
├── 🖼️ index.html              # Preview UI + toolbar + Recent dropdown
├── 📝 artifact.html           # Your artifact (overwrite each time)
├── 📂 history/                # Auto-backup of past artifacts
└── 📄 artifacts.json          # History manifest
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
