#!/usr/bin/env python3
"""
Artifact Preview Launcher v4.0 — Cross-platform Chrome launcher.

Auto-detects OS and launches Chrome with the preview window:
  - macOS: calls open-chrome.sh (unchanged, zero regression)
  - Windows: uses webbrowser + PyWinCtl for window control
  - Linux: xdg-open + PyWinCtl (or wmctrl fallback)

Usage:
  python3 launcher.py [portrait|horizontal|full|square|auto]
"""
import sys
import os
import webbrowser
import time

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
URL = f"http://localhost:{PORT}"

# Mode defaults
MODE = "auto"
if len(sys.argv) > 1:
    MODE = sys.argv[1].lower()
    if MODE not in ("portrait", "horizontal", "full", "square", "auto"):
        print(f"Unknown mode: {MODE}. Using 'auto'.")
        MODE = "auto"

PLATFORM = sys.platform


def launch_macos():
    """Launch Chrome on macOS using the existing open-chrome.sh script."""
    script_path = os.path.join(DIRECTORY, "open-chrome.sh")
    if not os.path.exists(script_path):
        print(f"Error: open-chrome.sh not found at {script_path}")
        return False
    import subprocess
    try:
        subprocess.run(["bash", script_path, MODE], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error launching Chrome: {e}")
        return False


def launch_windows():
    """Launch Chrome on Windows using webbrowser + PyWinCtl for window control."""
    try:
        import screeninfo
        import pywinctl
    except ImportError:
        print("Optional dependencies not installed.")
        print("For Windows, install: pip install screeninfo pywinctl")
        print("Falling back to basic webbrowser.open()...")
        webbrowser.open(URL)
        return True

    # Get primary monitor bounds
    try:
        monitors = screeninfo.get_monitors()
        primary = monitors[0] if monitors else None
    except Exception:
        primary = None

    # Chrome path patterns for Windows
    chrome_paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]

    chrome_exe = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_exe = path
            break

    if not chrome_exe:
        print("Chrome not found. Installing Chrome is recommended.")
        webbrowser.open(URL)
        return True

    # Build Chrome arguments
    chrome_args = [
        chrome_exe,
        "--new-window",
        f"--app={URL}",
        "--no-first-run",
        "--no-default-browser-check",
        "--user-data-dir=%TEMP%\\artifact-preview-chrome",
    ]

    # Window dimensions based on mode
    if primary:
        w, h = primary.width, primary.height
        if MODE == "portrait":
            width, height = min(430, int(w * 0.4)), min(844, int(h * 0.85))
            x, y = primary.x, primary.y
        elif MODE == "horizontal":
            width, height = min(1240, int(w * 0.85)), min(720, int(h * 0.7))
            x, y = primary.x, primary.y
        elif MODE == "full" or MODE == "auto":
            width, height = w, h
            x, y = primary.x, primary.y
        else:  # square
            width, height = min(960, int(w * 0.7)), min(800, int(h * 0.7))
            x = primary.x + (w - width) // 2
            y = primary.y + (h - height) // 2
    else:
        width, height, x, y = 960, 800, 100, 100

    # Launch Chrome
    import subprocess
    try:
        proc = subprocess.Popen(chrome_args)
        time.sleep(2)

        # Try to position window with PyWinCtl
        try:
            windows = pywinctl.getWindowsWithTitle("localhost")
            if windows:
                win = windows[0]
                if MODE in ("portrait", "horizontal", "square"):
                    win.moveTo(int(x), int(y))
                    win.resizeTo(int(width), int(height))
                if MODE == "full" or MODE == "auto":
                    win.maximize()
                win.activate()
        except Exception as e:
            print(f"Window positioning note: {e}")

        return True
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        return False


def launch_linux():
    """Launch Chrome on Linux using xdg-open + PyWinCtl (or wmctrl fallback)."""
    # Check for PyWinCtl
    try:
        import pywinctl
        has_pywinctl = True
    except ImportError:
        has_pywinctl = False
        print("Optional: pip install pywinctl for precise window control on Linux.")

    # Try to find Chrome
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/snap/bin/chromium",
    ]

    chrome_exe = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_exe = path
            break

    if not chrome_exe:
        print("Chrome not found. Trying xdg-open...")
        try:
            import subprocess
            subprocess.run(["xdg-open", URL], check=True)
            return True
        except subprocess.CalledProcessError:
            print("xdg-open failed. Please install Chrome.")
            return False

    # Try to get screen info
    width, height, x, y = 960, 800, 0, 0
    try:
        import screeninfo
        monitors = screeninfo.get_monitors()
        if monitors:
            primary = monitors[0]
            w, h = primary.width, primary.height
            if MODE == "portrait":
                width, height = min(430, int(w * 0.4)), min(844, int(h * 0.85))
                x, y = primary.x, primary.y
            elif MODE == "horizontal":
                width, height = min(1240, int(w * 0.85)), min(720, int(h * 0.7))
                x, y = primary.x, primary.y
            elif MODE == "full" or MODE == "auto":
                width, height = w, h
                x, y = primary.x, primary.y
            else:  # square
                width, height = min(960, int(w * 0.7)), min(800, int(h * 0.7))
                x = primary.x + (w - width) // 2
                y = primary.y + (h - height) // 2
    except ImportError:
        print("Optional: pip install screeninfo for precise window sizing on Linux.")

    # Build Chrome command
    chrome_args = [
        chrome_exe,
        "--new-window",
        f"--app={URL}",
        "--no-first-run",
        "--no-default-browser-check",
        "--user-data-dir=/tmp/artifact-preview-chrome",
        f"--window-size={width},{height}",
    ]

    if MODE in ("portrait", "horizontal", "square"):
        chrome_args.append(f"--window-position={x},{y}")

    # Launch Chrome
    import subprocess
    try:
        proc = subprocess.Popen(chrome_args)
        time.sleep(2)

        # Try to position window with PyWinCtl or wmctrl
        if has_pywinctl:
            try:
                windows = pywinctl.getWindowsWithTitle("localhost")
                if windows:
                    win = windows[0]
                    if MODE == "full" or MODE == "auto":
                        win.maximize()
                    else:
                        win.moveTo(int(x), int(y))
                        win.resizeTo(int(width), int(height))
                    win.activate()
            except Exception:
                pass
        else:
            # Try wmctrl as fallback
            try:
                subprocess.run(
                    ["wmctrl", "-r", "localhost", "-e", f"0,{int(x)},{int(y)},{int(width)},{int(height)}"],
                    capture_output=True
                )
            except FileNotFoundError:
                pass  # wmctrl not installed

        return True
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        return False


def main():
    print(f"Artifact Preview Launcher v4.0")
    print(f"Platform: {PLATFORM}")
    print(f"Mode: {MODE}")
    print(f"URL: {URL}")
    print()

    if PLATFORM == "darwin":
        print("Launching for macOS...")
        success = launch_macos()
    elif PLATFORM.startswith("win"):
        print("Launching for Windows...")
        success = launch_windows()
    else:
        print("Launching for Linux...")
        success = launch_linux()

    if success:
        print("Chrome launched successfully!")
    else:
        print("Launch may have failed. Check if Chrome is running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
