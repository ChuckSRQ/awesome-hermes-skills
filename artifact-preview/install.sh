#!/usr/bin/env bash
# Artifact Preview — one-line install
# Usage: curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.2/artifact-preview/install.sh | bash
set -euo pipefail

DEST_DIR="${ARTIFACT_PREVIEW_DIR:-$HOME/artifact-preview}"
PORT="${ARTIFACT_PREVIEW_PORT:-8765}"

case "$DEST_DIR" in
  "") echo "ERROR: DEST_DIR cannot be empty"; exit 1 ;;
  "$HOME") echo "ERROR: DEST_DIR cannot be $HOME"; exit 1 ;;
  "/") echo "ERROR: DEST_DIR cannot be /"; exit 1 ;;
  "$HOME"/*) ;;
  *) echo "ERROR: DEST_DIR must be under $HOME"; exit 1 ;;
esac

# Rollback on failure
trap 'echo "Install failed. Removing partial install..."; rm -rf "$DEST_DIR" 2>/dev/null; exit 1' ERR

BRANCH="${ARTIFACT_PREVIEW_BRANCH:-v4.2}"
REPO="https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/$BRANCH/artifact-preview"
SKILL_NAME="artifact-preview"

# ── Pre-flight checks ─────────────────────────────────────────────────────────

echo "Running pre-flight checks..."

if ! sw_vers >/dev/null 2>&1; then
  echo "ERROR: macOS required. Detected: $(sw_vers 2>/dev/null || echo 'unknown')"
  exit 1
fi

echo "  ✓ macOS OK"

# Robust Python 3.8+ check
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" || {
  echo "ERROR: Python 3.8+ required"
  exit 1
}
PYTHON_VERSION=$(python3 --version | sed 's/Python //')
echo "  ✓ Python $PYTHON_VERSION OK"

if command -v google-chrome >/dev/null 2>&1 || command -v chromium >/dev/null 2>&1 \
   || [ -d "/Applications/Google Chrome.app" ] || [ -d "$HOME/Applications/Google Chrome.app" ]; then
  echo "  ✓ Chrome OK"
else
  echo "ERROR: Google Chrome not found"
  echo "Download from https://www.google.com/chrome/"
  exit 1
fi

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

for file in index.html server.py launcher.py share-screenshot.py open-chrome.sh open-chrome.applescript SKILL.md README.md; do
  echo "  $file"
  curl -fsSL "$REPO/$file" -o "$DEST_DIR/$file"
done

chmod +x "$DEST_DIR/open-chrome.sh"
chmod +x "$DEST_DIR/launcher.py"
chmod +x "$DEST_DIR/share-screenshot.py"

echo "  ✓ All files downloaded"

# ── Register SKILL.md with Hermes ────────────────────────────────────────────

echo ""
echo "Registering skill with Hermes..."

if command -v hermes >/dev/null 2>&1; then
  hermes skills install --yes --category dev-platform "$SKILL_NAME" && echo "  ✓ hermes skills install succeeded" || {
    echo "  ⚠ hermes install failed, falling back to manual copy"
    HERMES_SKILL_DIR="$HOME/.hermes/skills/dev-platform/workspace/artifact-preview"
    mkdir -p "$HERMES_SKILL_DIR"
    cp "$DEST_DIR/SKILL.md" "$HERMES_SKILL_DIR/SKILL.md"
    echo "  ✓ SKILL.md copied to $HERMES_SKILL_DIR"
  }
else
  HERMES_SKILL_DIR="$HOME/.hermes/skills/dev-platform/workspace/artifact-preview"
  mkdir -p "$HERMES_SKILL_DIR"
  cp "$DEST_DIR/SKILL.md" "$HERMES_SKILL_DIR/SKILL.md"
  echo "  ✓ hermes not found — SKILL.md copied to $HERMES_SKILL_DIR"
fi

# ── Start server ─────────────────────────────────────────────────────────────

echo ""
echo "Starting Artifact Preview server..."

# Kill any existing server on port
if lsof -ti :$PORT >/dev/null 2>&1; then
  PID=$(lsof -ti :$PORT) && kill $PID 2>/dev/null
  sleep 1
fi

cd "$DEST_DIR"
nohup python3 server.py > "$DEST_DIR/server.log" 2>&1 &
SERVER_PID=$!

# Poll for readiness
READY=0
for i in $(seq 1 30); do
  if curl -sf "http://localhost:$PORT/" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" -eq 1 ]]; then
  echo "  ✓ Server running on http://localhost:$PORT (PID $SERVER_PID)"
else
  echo "ERROR: Server started (PID $SERVER_PID) but did not respond — check $DEST_DIR/server.log"
  kill $SERVER_PID 2>/dev/null || true
  exit 1
fi

# ── Post-install summary ─────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo " Artifact Preview installed successfully!"
echo "══════════════════════════════════════════════"
echo ""
echo "  Server:  http://localhost:$PORT"
echo "  Files:   $DEST_DIR"
echo "  Logs:    $DEST_DIR/server.log"
echo ""
echo "  To preview the current artifact, run:"
echo "  bash \"$DEST_DIR/open-chrome.sh\" auto"
echo ""
echo "──────────────────────────────────────────────"
echo " ONE-TIME SETUP (macOS Automation Permissions)"
echo ""
echo "  Open System Settings → Privacy & Security → Automation"
echo "  Grant Terminal permission to control Google Chrome."
echo ""
echo "  Or open directly:"
echo "  open \"x-apple.systempreferences:com.apple.preference.security?Privacy_Automation\""
echo "══════════════════════════════════════════════"
