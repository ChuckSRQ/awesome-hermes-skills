#!/usr/bin/env bash
# Artifact Preview browser launcher
# Usage: open-chrome.sh [portrait|horizontal|full]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mode="${1:-full}"
mode_norm="$(printf '%s' "$mode" | tr '[:upper:]' '[:lower:]' | tr -d "'" | xargs)"

case "$mode_norm" in
  portrait|horizontal|full) ;;
  *)
    printf 'Invalid mode: %s\nAllowed: portrait horizontal full\n' "$mode" >&2
    exit 2
    ;;
esac

osascript "$SCRIPT_DIR/open-chrome.applescript" "$mode_norm"
