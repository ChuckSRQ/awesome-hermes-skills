#!/usr/bin/env python3
"""
Artifact Preview v4 — Cross-Platform Launcher Skeleton
Auto-detects OS and launches Chrome with appropriate window control.
"""
import sys
import os
import webbrowser
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
URL = f"http://localhost:{PORT}"


def get_platform():
    """Detect the current operating system."""
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    elif sys.platform.startswith("linux"):
        return "linux"
    return "unknown"


def launch_macos(mode="auto"):
    """macOS: Use existing AppleScript approach via open-chrome.sh."""
    script_path = os.path.join(SCRIPT_DIR, "open-chrome.sh")
    if os.path.exists(script_path):
        subprocess.run(["bash", script_path, mode], check=True)
    else:
        # Fallback: direct osascript call
        applescript_path = os.path.join(SCRIPT_DIR, "open-chrome.applescript")
        if os.path.exists(applescript_path):
            subprocess.run(["osascript", applescript_path, mode], check=True)
        else:
            webbrowser.open(URL)


def launch_windows(mode="auto"):
    """Windows: Use webbrowser + PyWinCtl for Chrome window control."""
    try:
        import pywinctl as pwc
    except ImportError:
        print("[launcher] pywinctl not installed. Run: pip install pywinctl")
        webbrowser.open(URL)
        return

    # Open Chrome with target URL
    chrome_path = _find_chrome_windows()
    if not chrome_path:
        print("[launcher] Chrome not found, falling back to default browser")
        webbrowser.open(URL)
        return

    subprocess.Popen([chrome_path, "--new-window", URL])

    # Wait for window and position it
    _position_window_pwinctl(mode)


def launch_linux(mode="auto"):
    """Linux: Use xdg-open + PyWinCtl (or wmctrl fallback)."""
    # Try PyWinCtl first
    try:
        import pywinctl as pwc
        webbrowser.open(URL)
        _position_window_pwinctl(mode)
        return
    except ImportError:
        pass

    # Fallback: try wmctrl
    if _have_command("wmctrl"):
        _launch_linux_wmctrl(mode)
    else:
        print("[launcher] wmctrl not found. Run: pip install pywinctl or apt install wmctrl")
        webbrowser.open(URL)


def _position_window_pwinctl(mode):
    """Position Chrome window using PyWinCtl."""
    try:
        import pywinctl as pwc
        import time

        time.sleep(1.5)  # Give Chrome time to open and register

        chrome = None
        for w in pwc.getWindowsWithTitle("Chrome"):
            if URL in (w.URL or ""):
                chrome = w
                break

        if not chrome:
            # Try any Chrome window
            windows = pwc.getWindowsWithTitle("Chrome")
            if windows:
                chrome = windows[0]

        if chrome:
            # Apply mode-based sizing
            # portrait, horizontal, full, square (default)
            _apply_mode_to_window(chrome, mode)
        else:
            print("[launcher] Could not find Chrome window to position")
    except Exception as e:
        print(f"[launcher] Window positioning skipped: {e}")


def _apply_mode_to_window(window, mode):
    """Apply window sizing based on mode."""
    try:
        import pywinctl as pwc

        # Get primary monitor bounds
        try:
            monitor = pwc.getMouseMonitor()
        except Exception:
            monitor = pwc.getAllMonitors()[0] if pwc.getAllMonitors() else None

        if not monitor:
            return

        mode = mode or "square"
        mode_norm = mode.lower().strip()

        if mode_norm == "portrait":
            w, h = 400, 900
            x = monitor.x
            y = monitor.y
        elif mode_norm == "horizontal":
            w, h = 900, 600
            x = monitor.x
            y = monitor.y
        elif mode_norm == "full":
            window.maximize()
            return
        else:  # square or auto
            w, h = 600, 600
            x = monitor.x + (monitor.width - w) // 2
            y = monitor.y + (monitor.height - h) // 2

        window.moveTo(x, y)
        window.resizeTo(w, h)
    except Exception as e:
        print(f"[launcher] Mode apply failed: {e}")


def _launch_linux_wmctrl(mode):
    """Linux fallback using wmctrl for window control."""
    webbrowser.open(URL)

    import time
    time.sleep(1.5)

    # Try to get and position the Chrome window via wmctrl
    try:
        # Get Chrome window
        result = subprocess.run(
            ["wmctrl", "-l"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "Chrome" in line and URL in line:
                wid = line.split()[0]
                _apply_mode_wmctrl(wid, mode)
                return

        # Try any Chrome window
        for line in result.stdout.splitlines():
            if "Chrome" in line:
                wid = line.split()[0]
                _apply_mode_wmctrl(wid, mode)
                return
    except Exception as e:
        print(f"[launcher] wmctrl positioning failed: {e}")


def _apply_mode_wmctrl(wid, mode):
    """Apply window mode using wmctrl."""
    mode_norm = (mode or "square").lower().strip()

    if mode_norm == "full":
        subprocess.run(["wmctrl", "-i", "-r", wid, "-b", "add,maximized_vert,maximized_horz"])
    elif mode_norm == "portrait":
        subprocess.run(["wmctrl", "-i", "-r", wid, "-e", "0,0,0,400,900"])
    elif mode_norm == "horizontal":
        subprocess.run(["wmctrl", "-i", "-r", wid, "-e", "0,0,0,900,600"])
    else:
        # square
        subprocess.run(["wmctrl", "-i", "-r", wid, "-e", "0,0,0,600,600"])


def _find_chrome_windows():
    """Find Chrome executable path on Windows."""
    import winreg

    paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]

    for path in paths:
        if os.path.exists(path):
            return path
    return None


def _have_command(cmd):
    """Check if a command is available."""
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Artifact Preview Cross-Platform Launcher")
    parser.add_argument(
        "mode",
        nargs="?",
        default="auto",
        choices=["portrait", "horizontal", "full", "square", "auto"],
        help="Preview mode (default: auto)"
    )
    args = parser.parse_args()

    platform = get_platform()
    print(f"[launcher] Detected platform: {platform}")

    if platform == "macos":
        launch_macos(args.mode)
    elif platform == "windows":
        launch_windows(args.mode)
    elif platform == "linux":
        launch_linux(args.mode)
    else:
        print(f"[launcher] Unsupported platform: {platform}")
        webbrowser.open(URL)


if __name__ == "__main__":
    main()
