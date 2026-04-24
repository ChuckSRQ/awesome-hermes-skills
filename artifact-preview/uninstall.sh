#!/usr/bin/env bash
# Artifact Preview — uninstall
# Usage: curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/v4.3/artifact-preview/uninstall.sh | bash
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

echo "Uninstalling Artifact Preview..."

# 1. Stop server
if lsof -ti :$PORT >/dev/null 2>&1; then
  echo "  Stopping server..."
  PIDS=$(lsof -ti :$PORT 2>/dev/null) && [ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true
  sleep 1
  echo "  ✓ Server stopped"
else
  echo "  ✓ No server running"
fi

# 2. Remove runtime dir
if [[ -d "$DEST_DIR" ]]; then
  echo "  Removing $DEST_DIR..."
  rm -rf "$DEST_DIR"
  echo "  ✓ Runtime dir removed"
else
  echo "  ✓ No runtime dir found"
fi

# 3. Unregister from hermes
HERMES_SKILL_DIR="$HOME/.hermes/skills/dev-platform/workspace/artifact-preview"
if command -v hermes >/dev/null 2>&1; then
  hermes skills uninstall artifact-preview 2>/dev/null && echo "  ✓ hermes skill unregistered" || {
    rm -rf "$HERMES_SKILL_DIR"
    echo "  ✓ hermes skill removed (manual)"
  }
else
  rm -rf "$HERMES_SKILL_DIR"
  echo "  ✓ hermes skill removed"
fi

echo ""
echo "✓ Artifact Preview fully uninstalled."
