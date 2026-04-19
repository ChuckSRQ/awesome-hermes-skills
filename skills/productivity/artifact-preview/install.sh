#!/usr/bin/env bash
# Artifact Preview v3.1 — one-line install
# Usage: curl -fsSL https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/main/skills/productivity/artifact-preview/install.sh | bash
set -euo pipefail

DEST_DIR="${ARTIFACT_PREVIEW_DIR:-$HOME/artifact-preview}"
REPO="https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/main/skills/productivity/artifact-preview"

echo "Installing Artifact Preview v3.1 to $DEST_DIR ..."

mkdir -p "$DEST_DIR"

# Download all files
for file in index.html server.py share-screenshot.py open-chrome.sh open-chrome.applescript SKILL.md README.md; do
  echo "  $file"
  curl -fsSL "$REPO/$file" -o "$DEST_DIR/$file"
done

chmod +x "$DEST_DIR/open-chrome.sh"

echo ""
echo "Done. To start the server:"
echo "  cd $DEST_DIR && python3 server.py &"
echo ""
echo "Or add this to your shell profile for convenience:"
echo "  alias artifact-preview='cd $DEST_DIR && python3 server.py &'"
