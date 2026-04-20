---
name: artifact-preview
description: "🪽 Write code, see it live, instantly. Claude-style artifacts with persistent history, live reload, inline editor, screenshots, and 'Save as New'. v4.2 — one-line install! 🔥"
triggers:
  - preview
  - artifact
  - html preview
  - live preview
  - visual demo
  - ui preview
---

# 🪽 Artifact Preview **v4.2** — Live Preview + Smart History 🏆

**One-line install. Instant visual feedback. Every version safely saved. Zero "where did my work go?" 🔥**

## What This Is

This skill **shows the human** what you built — a UI, a dashboard, a page, a result. Visually. Instantly.

It is **not** for agents to read content from. The Chrome window is for human eyes only. Extract data directly from the source if needed.

## 🚀 One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash
```

Server starts automatically. You're ready to go. ✨

## How to Use

**Step 1 — Generate** complete, polished, self-contained HTML/CSS/JS (see Design Standards below).

**Step 2 — Save + trigger reload:**
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
    <!-- your complete content -->
</body>
</html>
ENDOFHTML

# Saves + archives + live reload — instant! ⚡
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null
```

**Step 3 — Open the preview:**
```bash
bash ~/artifact-preview/open-chrome.sh   # auto mode = magic 🪄
```

**Pro tip:** Always include `<title>` and `<h1>` — history labels depend on them.

**Pro tip:** Want to save a variation without losing the current preview? Use **"Save as New"** in the editor toolbar — it archives the variation without overwriting `artifact.html`. ✅

---

## 🎨 Design Standards

- ✅ **Complete, interactive, beautiful** — not skeletons 💀
- ✅ Self-contained single HTML file
- ✅ Light-first: `#F8F7F4` warm white background, `#8B5CF6` violet accent at ~10%
- ✅ Instrument Sans font, WCAG 4.5:1 contrast

---

## 🔥 Recommended Workflow (Copy-Paste This)

```bash
cd ~/artifact-preview
cat > artifact.html << 'ENDOFHTML'
[your complete, polished HTML/CSS/JS here]
ENDOFHTML

# Triggers save + archive + toast + live reload ⚡
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null

# Open — auto mode is pure magic 🪄
bash ~/artifact-preview/open-chrome.sh
```

---

## 📦 History — Never Lose Work 🛟

Every `/update` archives a new entry. Newest appear at top. Up to 15 kept.

- **Save** → overwrites `artifact.html` + archives → live preview updates
- **Save as New** → archives as new entry → does NOT overwrite `artifact.html`

Click any entry in the **Recent dropdown** to load it. Click **"● Current — Live"** to go back.

---

## 🪟 Launch Modes

```bash
bash ~/artifact-preview/open-chrome.sh            # auto-detect
bash ~/artifact-preview/open-chrome.sh portrait   # phone ~430×844 📱
bash ~/artifact-preview/open-chrome.sh horizontal # video ~1240×720 📺
bash ~/artifact-preview/open-chrome.sh full      # maximized 🖥️
```

**Always use `open-chrome.sh`** — NOT `open "http://..."` which ignores mode.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|:--------:|--------|
| `⌘⇧E` | Toggle HTML editor ✏️ |
| `⌘⇧S` | Save from editor 💾 |
| `⌘⇧R` | Refresh preview 🔄 |

---

## 📡 Server Commands

```bash
# Start server (runs in background)
cd ~/artifact-preview && python3 server.py &

# Stop server
PIDS=$(lsof -ti :8765 2>/dev/null) && [ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true

# Verify running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 ✅
```

### Endpoints

| Endpoint | Method | What it does |
|----------|--------|--------------|
| `/update` | POST | Save artifact.html + archive + live reload ⚡ |
| `/save-new` | POST | Archive as new version WITHOUT overwriting artifact.html |
| `/` | GET | Preview UI |
| `/artifact.html` | GET | Raw artifact HTML |
| `/artifacts.json` | GET | History manifest |
| `/events` | GET | SSE stream for live reload + history updates |
| `/history/<filename>` | GET | Serve archived artifact |

---

## 🛠️ Troubleshooting

**Server address already in use (Errno 48)?**
Server is already running. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/` → 200 means running.

**Preview not updating?**
Click **Refresh** in toolbar (instant via SSE) or restart: `PIDS=$(lsof -ti :8765 2>/dev/null) && [ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true && cd ~/artifact-preview && python3 server.py &`

**Content clipping — card shows only half:**
Fix CSS overflow: `body { overflow: auto }`, `#container { overflow: visible }`, `#preview-card { overflow: visible }`, `#artifact-frame { overflow: auto }`. Don't add `height: 100%` to `#preview-card`.

**Chrome window not opening (macOS)?**
Grant Automation permissions: **System Settings → Privacy & Security → Automation → Terminal → Google Chrome** ✅

**History dropdown empty after manual file copy?**
Terminal writes don't auto-archive. Use the editor **Save** button (POSTs to `/update`) or `/save-new` endpoint.

---

## 🆕 What's New in v4.2 🔥

- Newest versions at top of Recent dropdown
- Auto-save to history on server startup
- "✅ Saved to history" toast notifications
- "Save as New" button for safe variations
- Pinned "● Current — Live" in dropdown
