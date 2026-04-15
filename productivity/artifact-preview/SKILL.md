---
name: artifact-preview
description: Generate complete HTML/CSS/JS artifacts and open live previews in the browser instantly.
triggers:
  - make
  - build
  - show
  - create
  - generate
  - visual
  - interactive
  - app
  - dashboard
  - form
  - game
  - component
  - widget
  - page
  - ui
  - website
  - demo
---

# Artifact Preview — Live HTML/CSS/JS Preview in Browser

The user wants a "Claude Artifacts" experience: when asked for something visual or interactive, generate complete code and open a live, clickable preview instantly.

## How it works

- **Artifact server**: Python `http.server` running on a configurable directory at a configurable port (default `8765`)
- **Artifact file**: `index.html` — single self-contained HTML file with inline CSS/JS
- **Browser**: Opened via platform-appropriate command
- **Updates**: Overwrite `index.html`, browser auto-refreshes (or manually refresh)

## Trigger keywords

Any request containing: `make`, `build`, `show`, `create`, `generate`, `visual`, `interactive`, `app`, `dashboard`, `form`, `game`, `component`, `widget`, `page`, `ui`, `website`, `demo`

## Setup (one-time)

```bash
mkdir -p ~/artifact-preview
cd ~/artifact-preview && python3 -m http.server 8765 &
```

## Workflow for each request

1. **Generate** — Write complete, polished HTML/CSS/JS to `index.html` in the artifact directory. Use a single self-contained file with inline CSS/JS. Make it beautiful and interactive — not a skeleton.
2. **Save artifact** — After writing the file, extract a title from the content (from the `<h1>` or `<title>` tag). Check if an Obsidian vault exists at the configured path:
   - **If Obsidian exists**: Save the HTML to the configured artifacts directory, create an index note with frontmatter (`title`, `created`, `tags`) and a brief description linking back to the HTML file.
   - **If no Obsidian**: Save the HTML to the history folder instead.
   - Use `terminal` with a heredoc (`cat > file << 'EOF'`) to write files — it handles special characters better than write_file for large HTML content
3. **Open** — Open the browser at the preview URL. On macOS, use AppleScript to position the window:
```bash
osascript ~/artifact-preview/open-chrome.sh
```
The script opens the browser at 1/4 screen size, top-left position.
4. **Confirm** — Tell the user the preview is ready and they can interact with it. Mention they can refresh to see updates. If Obsidian is configured, mention the artifact was saved there.
5. **Update** — If the user requests changes ("make it brighter", "add dark mode", "change the button"), overwrite `index.html`, re-save to the same location (Obsidian if present, otherwise history folder), and tell the user to refresh.

## Design standards for artifacts

- **Complete code** — Not a skeleton, not a placeholder. Real working interactive app.
- **Beautiful by default** — Use modern CSS, good typography, nice colors, smooth animations.
- **Interactive** — Buttons work, inputs accept text, animations play.
- **Self-contained** — One HTML file, no external dependencies (except Google Fonts CDN if needed), no build step.
- **Responsive** — Works on laptop screens, not just desktop.
- **Use a consistent aesthetic** — Clean, modern, slightly playful. Good default palette to work from:
  - Background: `#0f172a` (dark slate) or `#f8fafc` (light)
  - Primary accent: `#6366f1` (indigo) or `#f59e0b` (amber)
  - Cards: semi-transparent with `backdrop-filter: blur`
  - Font: system-ui or Inter from Google Fonts
  - Rounded corners, subtle shadows, smooth transitions

## Artifact storage

**With Obsidian:**
- Artifact HTML: `<obsidian-vault>/03-Notes/artifacts/YYYY-MM-DD-slugified-title.html`
- Artifact index: `<obsidian-vault>/03-Notes/artifacts/YYYY-MM-DD-slugified-title.md`

**Without Obsidian (fallback):**
- Artifact HTML: `<artifact-preview-dir>/history/YYYY-MM-DD-slugified-title.html`

## File locations (configurable)

- Artifact directory: `~/artifact-preview/` (or custom path)
- Artifact file: `index.html` inside the artifact directory
- HTTP server port: `8765` (configurable)
- Preview URL: `http://localhost:8765`

## Server management

- Server should already be running from setup
- To restart if needed: `pkill -f "http.server 8765"` then `cd ~/artifact-preview && python3 -m http.server 8765 &`
- To verify it's running: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/`
