---
name: artifact-preview
description: "🪽 Write code, see it live, instantly. Claude-style artifacts with reliable persistent history, live reload, inline editor, screenshots, and 'Save as New'. v4.2"
triggers:
  - make
  - build
  - show
  - create
  - generate
  - visual
  - interactive
  - dashboard
  - app
  - ui
  - website
  - demo
---

# Artifact Preview **v4.2** — Live Preview + Smart History 🏆

**One-line install.** Instant visual feedback. Every version safely saved.

### 🔥 Recommended Workflow (Copy-Paste This)

```bash
cd ~/artifact-preview

cat &gt; artifact.html &amp;lt;&lt; 'ENDOFHTML'
[your complete, polished HTML/CSS/JS here]
ENDOFHTML

# Triggers save + archive + toast + live reload
curl -X POST http://localhost:8765/update \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @artifact.html -s -o /dev/null
```

Then open the preview:
```bash
bash ~/artifact-preview/open-chrome.sh
```

**Pro tip for users**: Click **“Save as New”** in the editor toolbar when you want to save a variation without changing the current live preview.

### What’s New in v4.2
- Newest versions now appear at the top of Recent dropdown
- Auto-save to history on server startup
- “Saved to history” toast notifications
- “Save as New” button for safe variations
- Pinned “● Current — Live” in dropdown

(Keep your existing sections for launch modes, design standards, keyboard shortcuts, troubleshooting, etc.)

---

