#!/usr/bin/env bash
# Artifact Preview browser launcher
# Usage: open-chrome.sh [portrait|horizontal|full|auto]
# Default (no args): auto-detect from artifact.html meta tag or content
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT="$SCRIPT_DIR/artifact.html"

mode="${1:-auto}"
mode_norm="$(printf '%s' "$mode" | tr '[:upper:]' '[:lower:]' | tr -d "'" | xargs)"

detect_mode() {
  local artifact="$1"

  if [[ ! -f "$artifact" ]]; then
    printf 'full'
    return
  fi

  # 1. Explicit meta tag: <meta name="preview-mode" content="portrait|horizontal|full">
  local meta_mode
  meta_mode="$(grep -oiE 'meta\s+name="preview-mode"\s+content="(portrait|horizontal|full)"' "$artifact" 2>/dev/null | grep -oE '(portrait|horizontal|full)' | head -1 || true)"
  if [[ -n "$meta_mode" ]]; then
    printf '%s' "$meta_mode"
    return
  fi

  # 2. Full-page indicators (nav, footer, header) — beats viewport check
  if grep -qiE '<nav|<footer|<header' "$artifact" 2>/dev/null; then
    printf 'full'
    return
  fi

  # 3. Mobile viewport + narrow content → portrait
  if grep -qiE 'viewport.*width=device-width' "$artifact" 2>/dev/null; then
    if grep -qiE 'min-height:\s*100vh|max-width:\s*(4[0-9]{2}|[1-3][0-9]{2})px' "$artifact" 2>/dev/null; then
      printf 'portrait'
      return
    fi
  fi

  # 4. Default: horizontal
  printf 'horizontal'
}

case "$mode_norm" in
  portrait|horizontal|full)
    ;;
  auto)
    mode_norm="$(detect_mode "$ARTIFACT")"
    ;;
  *)
    printf 'Invalid mode: %s\nAllowed: portrait horizontal full auto\n' "$mode" >&2
    exit 2
    ;;
esac

osascript "$SCRIPT_DIR/open-chrome.applescript" "$mode_norm"
