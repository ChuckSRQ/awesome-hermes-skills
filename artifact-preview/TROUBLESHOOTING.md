# Artifact Preview — Troubleshooting Log

*Last updated: 2026-04-24 | Branch: feat/artifact-preview-v4.3 | PR: #27*

---

## Issue: Chrome profile picker appearing on cold start

**Symptoms:** When Chrome is not running and the AppleScript launches it, a profile picker dialog appears, blocking the preview.

**Root cause:** Newer Chrome versions on this system show the profile picker by default on first launch without a URL argument.

**Fix:** Added `--args --profile-directory=Default` to the cold-start `open` command:

```applescript
do shell script "open -a 'Google Chrome' --args --profile-directory=Default " & quoted form of previewURL
```

This forces Chrome to skip the profile picker and open directly to the preview URL.

---

## Issue: Chrome reusing existing window instead of creating new one

**Symptoms:** When Chrome is already running, the AppleScript would bring the existing window to front instead of opening a new one.

**Root cause:** `activate` was called at the top of the AppleScript `tell application "Google Chrome"` block. This caused Chrome to focus its existing window before `make new window` was called, making Chrome reuse that window instead of creating a new one.

**Fix:** Moved `activate` to AFTER `make new window` and `set bounds`:

```applescript
tell application "Google Chrome"
    if didColdStart is false then
        activate          -- was here before (WRONG)
        make new window
        delay 0.15
        set URL of active tab of front window to previewURL
    end if

    delay 0.1

    if theMode is "portrait" then
        set bounds of front window to {60, 60, 540, 1020}
    else if theMode is "horizontal" then
        set bounds of front window to {60, 60, 1340, 780}
    else
        -- full screen
    end if

    activate           -- now here (CORRECT)
end tell
```

---

## Issue: Duplicate tab on cold start

**Symptoms:** When Chrome was cold-started with `open -a 'Google Chrome' <url>`, a new window opened with the URL already loaded, but `make new window` was still called, creating a duplicate tab.

**Root cause:** The cold-start path opens Chrome with the URL already loaded in the first window. Calling `make new window` afterwards creates a second tab instead of using the first one.

**Fix:** Added `didColdStart` flag — when Chrome was not running, skip `make new window`:

```applescript
set didColdStart to false

if not chromeRunning then
    do shell script "open -a 'Google Chrome' --args --profile-directory=Default " & quoted form of previewURL
    delay 2.0
    set didColdStart to true
end if

tell application "Google Chrome"
    if didColdStart is false then
        make new window      -- only when Chrome was already running
        delay 0.15
        set URL of active tab of front window to previewURL
    end if
```

---

## Issue: SSE live reload not working

**Symptoms:** Changes to artifact.html did not trigger auto-reload in the preview.

**Root cause:** `~/artifact-preview/index.html` (the preview UI wrapper, 905 lines) was overwritten by a different project (Sofia storybook, 1361 lines). The overwritten file lacked the `EventSource` listener that receives the SSE `reload` event.

**Fix:** Restored `index.html` from the repo source (`~/awesome-hermes-skills/artifact-preview/index.html`).

**Verification:** After restoring, verified with:
```bash
curl -X POST http://localhost:8765/update -d "<h1>test</h1>" -H "Content-Type: text/html"
# SSE listener received: event: reload
```

---

## Issue: History dropdown preview and code panel out of sync

**Symptoms:** Using the — Recent — dropdown to switch to a previous artifact changed the preview iframe correctly but the code panel (Code tab) still showed the current artifact's source.

**Root cause:** The dropdown change handler only updated `artifactFrame.src` — it never fetched the history artifact's source HTML into the textarea.

**Fix:** Updated the dropdown `change` handler to also fetch and load the history artifact's source:

```javascript
recentDropdown.addEventListener('change', async () => {
    const filename = recentDropdown.value;
    if (!filename) {
        artifactFrame.src = 'artifact.html?t=' + Date.now();
        if (editorOpen()) {
            const resp = await fetch('artifact.html');
            editorTextarea.value = await resp.text();
        }
        return;
    }
    const src = '/history/' + filename + '?t=' + Date.now();
    artifactFrame.src = src;
    if (editorOpen()) {
        const resp = await fetch(src.replace('?t=' + Date.now(), ''));
        editorTextarea.value = await resp.text();
    }
});
```

---

## Window size decisions

### Portrait: 480 × 960 px (9:16)
- Bounds: `{60, 60, 540, 1020}` → content area 480×960
- All content visible without scrolling
- The narrowest width that fit the test artifact content without vertical scroll

### Horizontal: 1280 × 720 px (16:9)
- Bounds: `{60, 60, 1340, 780}` → content area 1280×720
- Standard 16:9 resolution

### Final AppleScript bounds

```applescript
if theMode is "portrait" then
    set bounds of front window to {60, 60, 540, 1020}   -- 480×960
else if theMode is "horizontal" then
    set bounds of front window to {60, 60, 1340, 780}  -- 1280×720
else
    -- full: NSScreen main screen dimensions
```

---

## Key files

| File | Purpose |
|------|---------|
| `open-chrome.applescript` | Chrome launcher — contains all window sizing and Chrome startup logic |
| `index.html` | Preview UI wrapper — SSE listener, toolbar, code panel, history dropdown |
| `server.py` | HTTP server — artifact serving, SSE broadcast, history management |
| `artifact.html` | The active artifact being previewed |
| `history/` | Archived artifact versions |

## Testing checklist

After any AppleScript change:
1. Quit Chrome completely (`pkill -9 "Google Chrome"`)
2. Run `osascript open-chrome.applescript portrait`
3. Verify: 1 window, 1 tab, no profile picker, correct bounds
4. Test warm start (Chrome already open): `osascript open-chrome.applescript horizontal`
5. Verify: new window opens, existing windows untouched

After any index.html change:
1. Restart server: `pkill -f "server.py"` + `python3 server.py`
2. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/` returns 200
3. Open Chrome and test history dropdown switching
