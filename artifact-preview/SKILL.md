---
name: artifact-preview
description: "🪽 Write code, see it live, instantly. Claude-style artifacts with persistent history, live reload, inline editor, screenshots, and 'Save as New'. v4.3 — one-line install! 🔥"
triggers:
  - preview
  - artifact
  - html preview
  - live preview
  - visual demo
  - ui preview
---

# 🪽 Artifact Preview **v4.3** — Live Preview + Smart History 🏆

**One-line install. Instant visual feedback. Every version safely saved. Zero "where did my work go?" 🔥**

## What This Is

This skill **shows the human** what you built — a UI, a dashboard, a page, a result. Visually. Instantly.

It is **not** for agents to read content from. The Chrome window is for human eyes only. Extract data directly from the source if needed.

**⚠️ INCOMPATIBLE with chrome-devtools. Never use both simultaneously.**

## 🚀 One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.3/artifact-preview/install.sh | bash
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

**⚠️ Static asset trap — images and subdirectories:** If your artifact HTML references subdirectories or image files (e.g. `<img src="slides/slide-01.jpg">`), those files MUST be inside `~/artifact-preview/` — the server only serves from its own directory. Files elsewhere on the filesystem are invisible even if they exist. Always copy assets to `~/artifact-preview/` before POSTing.

**⚠️ Pitfall — tilde in curl `@` syntax:** `curl --data-binary @~/path` fails because `~` doesn't expand through curl's `@` filename operator. Always `cd` to the directory first, or copy to a temp file with absolute path first:
```bash
cp ~/artifact-preview/history/myfile.html /tmp/myfile.html
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @/tmp/myfile.html -s -o /dev/null
```

**⚠️ NEVER POST test strings to `/update` with `@filepath`.** If you POST `"test"` (or any short string) using `--data-binary "test"` or `@/path/to/small-file`, the server writes that content directly to `artifact.html` on disk — overwriting whatever was there. Subsequent `@artifact.html` POSTs will then re-upload the corrupted content. Symptom: POST returns HTTP 200 but the page still shows the old/corrupted content. Fix: re-write the correct content to disk with `write_file`, then POST with `@filepath`.

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

**Viewing a file from history (not a new artifact)?** Copy it to artifact.html first, then open:
```bash
cp ~/artifact-preview/history/<filename.html> ~/artifact-preview/artifact.html
bash ~/artifact-preview/open-chrome.sh portrait   # or horizontal / full
```

---

## 📦 History — Never Lose Work 🛟

Every `/update` archives a new entry. Newest appear at top. Up to 15 kept.

- **Save** → overwrites `artifact.html` + archives → live preview updates
- **Save as New** → archives as new entry → does NOT overwrite `artifact.html`

Click any entry in the **Recent dropdown** to load it. Click **"● Current — Live"** to go back.

---

**🪟 Launch Modes**

```bash
bash ~/artifact-preview/open-chrome.sh            # auto-detect — MUST use bash, not open
bash ~/artifact-preview/open-chrome.sh portrait   # phone 480×960 (9:16) 📱
bash ~/artifact-preview/open-chrome.sh horizontal # monitor 1280×720 (16:9) 📺
bash ~/artifact-preview/open-chrome.sh full      # maximized 🖥️
```

**⚠️ Always use `bash ~/artifact-preview/open-chrome.sh` — NOT `open ~/artifact-preview/open-chrome.sh`.** The `open` command on macOS treats the script path as a file to open in the default app, not as a shell script to execute. `bash` runs it properly with arguments passed through.

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
| `/` | GET | Preview UI |
| `/artifact.html` | GET | Raw artifact HTML |
| `/artifacts.json` | GET | History manifest |
| `/events` | GET | SSE stream for live reload + history updates |
| `/history/<filename>` | GET | Serve archived artifact |

---

## 🛠️ Troubleshooting

**Server address already in use (Errno 48)?**
The `lsof -ti :8765 | xargs kill` pattern can silently fail if the process is zombie or orphaned. Use this instead:
```bash
# Find the actual PID holding the port
lsof -i :8765
# Example output: COMMAND  PID      USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
#                  Python  9273 carlosmac    4u  IPv4 0xeddad3b3e14e8540      0t0  TCP *:ultraseek-http (LISTEN)

# Force-kill it
kill -9 <PID>

# Verify port is free
lsof -i :8765  # should return nothing

# Restart fresh
cd ~/artifact-preview && python3 server.py &
sleep 3
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 ✅
```

Or verify server is already running (Errno 48 means it's already up):
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 means running ✅
```

**Server appears alive (port 8765 responds) but POST returns empty / curl error 52?**
The server process is hung — it accepts connections but can't process requests. Symptoms: `curl -X POST http://localhost:8765/update` returns "Empty reply from server" (curl error 52) even though `GET /` returns 200. Fix: kill and restart from scratch:
```bash
# Kill hung server
PIDS=$(lsof -ti :8765 2>/dev/null) && [ -n "$PIDS" ] && kill $PIDS
sleep 1

# Restart fresh
cd ~/artifact-preview && python3 server.py &
sleep 2
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 ✅
```

**Preview not updating?**
Click **Refresh** in toolbar (instant via SSE) or restart: `PIDS=$(lsof -ti :8765 2>/dev/null) && [ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true && cd ~/artifact-preview && python3 server.py &`

**Content clipping — card shows only half:**
Fix CSS overflow: `body { overflow: auto }`, `#container { overflow: visible }`, `#preview-card { overflow: visible }`, `#artifact-frame { overflow: auto }`. Don't add `height: 100%` to `#preview-card`.

**Chrome window not opening (macOS)?**
Grant Automation permissions: **System Settings → Privacy & Security → Automation → Terminal → Google Chrome** ✅

**History dropdown empty after manual file copy?**
Terminal writes don't auto-archive. Use the editor **Save** button (POSTs to `/update`) or manually POST to `/update`.

**History stops saving across server restarts — POSTs return 200 but nothing is archived?**
If `history/` exists but `artifacts.json` does NOT, `_archive_artifact()` silently fails. The server appears to work (POST returns 200) but nothing gets saved. Symptoms: `ls history/` is empty or stale, `artifacts.json` is missing or outdated.

**Fix:** Kill the old server and start fresh:
```bash
# Find and kill old server
OLD_PID=$(lsof -ti :8765 2>/dev/null)
[ -n "$OLD_PID" ] && kill $OLD_PID
sleep 1

# Restart — fresh server writes artifacts.json correctly
cd ~/artifact-preview && python3 server.py &
sleep 2
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
# → 200 ✅
```

---

## 🆕 What's New in v4.3 🔥

- **Fixed:** SSE live-reload — the preview UI now correctly listens for `reload` events and refreshes the artifact iframe instantly after every POST
- **Fixed:** Server-side broadcast reliability — verified that `event: reload` fires from `/events` SSE endpoint after every `/update` POST
- **Fixed:** Chrome startup reliability — profile picker suppressed on cold start, no duplicate tabs when Chrome already running, window activation fixed
- **Fixed:** Dual-panel history recall — switching to a past artifact via the Recent dropdown now updates BOTH the preview iframe AND the code panel simultaneously
- **Improved:** Precise window sizing — Portrait 480×960 (9:16), Horizontal 1280×720 (16:9), all content visible without scrolling

---

## 🆕 What's New in v4.2 🔥

- Newest versions at top of Recent dropdown
- Auto-save to history on server startup
- "✅ Saved to history" toast notifications
- "Save as New" button for safe variations
- Pinned "● Current — Live" in dropdown
