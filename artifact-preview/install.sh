#!/usr/bin/env bash
# Artifact Preview — one-line install
# Usage: curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/main/artifact-preview/install.sh | bash
set -euo pipefail

DEST_DIR="${ARTIFACT_PREVIEW_DIR:-$HOME/artifact-preview}"
REPO="https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/main/artifact-preview"
SKILL_NAME="ChuckSRQ/awesome-hermes-skills/artifact-preview"

# ── Pre-flight checks ─────────────────────────────────────────────────────────

echo "Running pre-flight checks..."

if ! sw_vers >/dev/null 2>&1; then
  echo "ERROR: macOS required. Detected: $(sw_vers 2>/dev/null || echo 'unknown')"
  exit 1
fi

PYTHON_MIN="3.8"
PYTHON_VERSION=$(python3 --version 2>/dev/null | sed 's/Python //' | cut -d. -f1,2)
if [[ -z "$PYTHON_VERSION" ]]; then
  echo "ERROR: Python 3 not found. Install from https://www.python.org/"
  exit 1
fi
if [[ "$(printf '%s\n' "$PYTHON_MIN" "$PYTHON_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN" ]]; then
  echo "ERROR: Python $PYTHON_MIN+ required, found $PYTHON_VERSION"
  exit 1
fi

if [[ ! -d "/Applications/Google Chrome.app" ]]; then
  echo "ERROR: Google Chrome not found at /Applications/Google Chrome.app"
  echo "Download from https://www.google.com/chrome/"
  exit 1
fi

echo "  ✓ macOS OK"
echo "  ✓ Python $PYTHON_VERSION OK"
echo "  ✓ Chrome OK"

# ── Idempotency: backup existing artifact.html ────────────────────────────────

mkdir -p "$DEST_DIR/history"

if [[ -f "$DEST_DIR/artifact.html" ]]; then
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  cp "$DEST_DIR/artifact.html" "$DEST_DIR/history/artifact-$TIMESTAMP.html"
  echo "Backed up existing artifact.html → history/artifact-$TIMESTAMP.html"
fi

# ── Download runtime files ────────────────────────────────────────────────────

echo ""
echo "Downloading Artifact Preview files..."

for file in index.html server.py share-screenshot.py open-chrome.sh open-chrome.applescript SKILL.md README.md; do
  echo "  $file"
  curl -fsSL "$REPO/$file" -o "$DEST_DIR/$file"
done

chmod +x "$DEST_DIR/open-chrome.sh"
chmod +x "$DEST_DIR/share-screenshot.py"

echo "  ✓ All files downloaded"

# ── Register SKILL.md with Hermes ────────────────────────────────────────────

echo ""
echo "Registering skill with Hermes..."

if command -v hermes >/dev/null 2>&1; then
  hermes skills install --yes "$SKILL_NAME" 2>/dev/null && echo "  ✓ hermes skills install succeeded" || {
    echo "  ⚠ hermes install failed, falling back to manual copy"
    HERMES_SKILL_DIR="$HOME/.hermes/skills/productivity/artifact-preview"
    mkdir -p "$HERMES_SKILL_DIR"
    cp "$DEST_DIR/SKILL.md" "$HERMES_SKILL_DIR/SKILL.md"
    echo "  ✓ SKILL.md copied to $HERMES_SKILL_DIR"
  }
else
  HERMES_SKILL_DIR="$HOME/.hermes/skills/productivity/artifact-preview"
  mkdir -p "$HERMES_SKILL_DIR"
  cp "$DEST_DIR/SKILL.md" "$HERMES_SKILL_DIR/SKILL.md"
  echo "  ✓ hermes not found — SKILL.md copied to $HERMES_SKILL_DIR"
fi

# ── Start server ─────────────────────────────────────────────────────────────

echo ""
echo "Starting Artifact Preview server..."

# Kill any existing server on port 8765
if lsof -ti :8765 >/dev/null 2>&1; then
  pkill -f "python3.*server.py" 2>/dev/null || true
  sleep 1
fi

cd "$DEST_DIR"
nohup python3 server.py > /tmp/artifact-preview.log 2>&1 &
SERVER_PID=$!

# Poll for readiness
READY=0
for i in $(seq 1 10); do
  if curl -sf --unix-socket /dev/null "http://localhost:8765/" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 0.5
done

if [[ "$READY" -eq 1 ]]; then
  echo "  ✓ Server running on http://localhost:8765 (PID $SERVER_PID)"
else
  echo "  ⚠ Server started (PID $SERVER_PID) but not responding — check /tmp/artifact-preview.log"
fi

# ── Post-install summary ─────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo " Artifact Preview installed successfully!"
echo "══════════════════════════════════════════════"
echo ""
echo "  Server:  http://localhost:8765"
echo "  Files:   $DEST_DIR"
echo "  Logs:    /tmp/artifact-preview.log"
echo ""
echo "  To preview an artifact, run:"
echo "  artifact-preview <artifact-file>"
echo ""
echo "──────────────────────────────────────────────"
echo " ONE-TIME SETUP (macOS Automation Permissions)"
echo ""
OPEN_URL="x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
echo "  Open System Settings → Privacy & Security → Automation"
echo "  Grant Terminal permission to control Google Chrome."
echo ""
echo "  Or open directly:"
echo "  open \"$OPEN_URL\""
echo "══════════════════════════════════════════════"
