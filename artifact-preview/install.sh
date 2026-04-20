#!/usr/bin/env bash
# Artifact Preview v4.2 — One-line magic install for Hermes Agent

set -euo pipefail

VERSION="v4.2"
DEST_DIR="${ARTIFACT_PREVIEW_DIR:-$HOME/artifact-preview}"
REPO="https://raw.githubusercontent.com/ChuckSRQ/awesome-hermes-skills/main/skills/productivity/artifact-preview"

echo "🪽 Installing Artifact Preview ${VERSION}..."

mkdir -p "$DEST_DIR"

echo "📥 Downloading latest files..."
for file in server.py launcher.py open-chrome.sh open-chrome.applescript share-screenshot.py index.html README.md SKILL.md; do
  echo "   → $file"
  curl -fsSL "$REPO/$file" -o "$DEST_DIR/$file"
done

chmod +x "$DEST_DIR/open-chrome.sh" "$DEST_DIR/launcher.py"

echo ""
echo "✅ Artifact Preview ${VERSION} installed successfully to $DEST_DIR"
echo ""
echo "🚀 Quick start:"
echo "   cd $DEST_DIR && python3 server.py &"
echo "   bash $DEST_DIR/open-chrome.sh          # auto mode = magic"
echo ""
echo "💡 Pro tip: Add this alias to your ~/.zshrc or ~/.bashrc"
echo "   alias ap='cd $DEST_DIR && python3 server.py &'"
echo ""
echo "🔥 You're all set! Live reload, persistent history, 'Save as New', and beautiful toasts are ready. Go build something awesome! 🪽"
