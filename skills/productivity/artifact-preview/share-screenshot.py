#!/usr/bin/env python3
"""
Screenshot share helper v2.
Receives base64 PNG on stdin, saves to ~/Downloads, opens Preview.
Preview has a built-in Share button — one click to AirDrop, Messages, Mail, etc.
"""
import sys
import base64
import os
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    data = sys.stdin.read().strip()
    if not data:
        print("No data received", file=sys.stderr)
        sys.exit(1)

    # Decode
    try:
        png_data = base64.b64decode(data + '==')  # padding if needed
    except Exception as e:
        print(f"Decode error: {e}", file=sys.stderr)
        sys.exit(1)

    # Save to Downloads
    ts = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    filename = f"artifact-screenshot-{ts}.png"
    downloads = Path.home() / "Downloads"
    filepath = downloads / filename

    with open(filepath, 'wb') as f:
        f.write(png_data)

    print(f"Saved: {filepath}")

    # Open in Preview (has Share button in toolbar)
    subprocess.Popen(['open', '-a', 'Preview', str(filepath)])

if __name__ == '__main__':
    main()
