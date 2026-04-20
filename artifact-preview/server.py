#!/usr/bin/env python3
"""
Artifact Preview Server v4.0 — Fast caching HTTP server with SSE for live updates.
Routes:
  /              → UI wrapper (index.html)
  /artifact      → raw artifact HTML content (served as-is)
  /update        → POST to save updated artifact HTML
  /events        → SSE stream for live reload signals
  /notify-open    → POST to trigger browser auto-open
  /history/<filename> → serve archived artifact files
  /artifacts.json → history manifest
"""
import http.server
import socketserver
import os
import hashlib
import time
import signal
import json
import threading
import subprocess
import re

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(DIRECTORY, "index.html")
ARTIFACT_FILE = os.path.join(DIRECTORY, "artifact.html")
ARTIFACTS_JSON = os.path.join(DIRECTORY, "artifacts.json")
HISTORY_DIR = os.path.join(DIRECTORY, "history")
MAX_HISTORY = 15

# In-memory cache
_cached_index = None
_cached_artifact = None
_cached_etag_index = None
_cached_etag_artifact = None
_mtime_index = 0
_mtime_artifact = 0

# SSE clients for live reload
_sse_clients = []
_sse_lock = threading.Lock()

# Pending auto-open flag
_pending_open = {"mode": "square"}
_open_lock = threading.Lock()

# History management
_history = []
_history_lock = threading.Lock()


def _extract_title(html_content):
    """Extract <title> or first <h1> from HTML for readable label."""
    if not html_content:
        return None
    # Try <title> first
    match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try first <h1>
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _slugify(title):
    """Convert title to URL-safe filename slug."""
    if not title:
        return "untitled"
    # Remove HTML tags
    title = re.sub(r'<[^>]+>', '', title)
    # Keep only alphanumeric, spaces, hyphens
    slug = re.sub(r'[^a-zA-Z0-9\s\-]', '', title)
    # Replace spaces with hyphens and lowercase
    slug = '-'.join(slug.split())[:50]
    return slug.lower() or "untitled"


def _load_history():
    """Load history manifest from artifacts.json."""
    global _history
    with _history_lock:
        if os.path.exists(ARTIFACTS_JSON):
            try:
                with open(ARTIFACTS_JSON, "r", encoding="utf-8") as f:
                    _history = json.load(f)
            except (json.JSONDecodeError, IOError):
                _history = []
        else:
            _history = []


def _save_history():
    """Save history manifest to artifacts.json."""
    with _history_lock:
        try:
            with open(ARTIFACTS_JSON, "w", encoding="utf-8") as f:
                json.dump(_history, f, indent=2)
        except IOError as e:
            print(f"[{time.strftime('%H:%M:%S')}] Failed to save history: {e}")


def _archive_artifact():
    """Copy current artifact.html to history/<timestamp>-<slug>.html, prune oldest beyond MAX_HISTORY."""
    global _history

    if not os.path.exists(ARTIFACT_FILE):
        return

    # Read current artifact
    try:
        with open(ARTIFACT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except IOError:
        return

    # Extract title and create slug
    title = _extract_title(content)
    slug = _slugify(title)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{slug}.html"
    filepath = os.path.join(HISTORY_DIR, filename)

    # Ensure history directory exists
    os.makedirs(HISTORY_DIR, exist_ok=True)

    # Write archived file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError:
        return

    # Update history list
    with _history_lock:
        # Remove existing entry with same filename (if any)
        _history = [h for h in _history if h.get("filename") != filename]
        # Add new entry at the front
        _history.insert(0, {
            "filename": filename,
            "title": title or "Untitled",
            "timestamp": int(time.time()),
            "path": filepath
        })
        # Prune oldest beyond MAX_HISTORY
        if len(_history) > MAX_HISTORY:
            pruned = _history[MAX_HISTORY:]
            _history = _history[:MAX_HISTORY]
            # Remove pruned files from disk
            for item in pruned:
                try:
                    if os.path.exists(item.get("path", "")):
                        os.remove(item.get("path", ""))
                except OSError:
                    pass

    _save_history()

    # Notify frontend for nice toast
    _notify_clients("history-saved", {"title": title or "Untitled"})

    # Broadcast history-update to all SSE clients
    _broadcast_history_update()


def _broadcast_history_update():
    """Broadcast history-update SSE event with full items list."""
    with _history_lock:
        items = [{"filename": h["filename"], "title": h["title"], "timestamp": h["timestamp"]} for h in _history]
    payload = json.dumps({"type": "history-update", "items": items})
    msg = f"event: history-update\ndata: {payload}\n\n"
    with _sse_lock:
        dead = []
        for client in _sse_clients:
            try:
                client(msg.encode("utf-8"))
            except Exception:
                dead.append(client)
        for client in dead:
            _sse_clients.remove(client)


def _read_file(path, cache_tuple):
    """Read file into cache if mtime changed. Returns (content_bytes, cache_tuple)."""
    cached_content, cached_etag, cached_mtime = cache_tuple
    try:
        mtime = os.stat(path).st_mtime
        if mtime != cached_mtime:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            content_bytes = content.encode("utf-8")
            etag = hashlib.md5(content_bytes).hexdigest()[:16]
            print(f"[{time.strftime('%H:%M:%S')}] Reloaded {os.path.basename(path)} ({len(content_bytes):,} bytes)")
            return content_bytes, (content_bytes, etag, mtime)
        return cached_content, cache_tuple
    except FileNotFoundError:
        return cached_content, cache_tuple


def read_index():
    global _cached_index, _cached_etag_index, _mtime_index
    _cached_index, (_c, _e, _m) = _read_file(INDEX_FILE, (_cached_index, _cached_etag_index, _mtime_index))
    _cached_etag_index, _mtime_index = _e, _m
    return _cached_index


def read_artifact():
    global _cached_artifact, _cached_etag_artifact, _mtime_artifact
    _cached_artifact, (_c, _e, _m) = _read_file(ARTIFACT_FILE, (_cached_artifact, _cached_etag_artifact, _mtime_artifact))
    _cached_etag_artifact, _mtime_artifact = _e, _m
    return _cached_artifact


def _notify_clients(event_type, data=None):
    """Broadcast event to all SSE clients."""
    payload = json.dumps({"type": event_type, **(data or {})})
    msg = f"event: {event_type}\ndata: {payload}\n\n"
    with _sse_lock:
        dead = []
        for client in _sse_clients:
            try:
                client(msg.encode("utf-8"))
            except Exception:
                dead.append(client)
        for client in dead:
            _sse_clients.remove(client)


class Handler(http.server.SimpleHTTPRequestHandler):
    directory = DIRECTORY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            content = read_index()
            self._send(200, "text/html; charset=utf-8", content)
        elif self.path == "/artifact" or self.path == "/artifact.html":
            content = read_artifact()
            self._send(200, "text/html; charset=utf-8", content)
        elif self.path == "/events":
            # SSE stream for live reload
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            def sender(data):
                self.wfile.write(data)
                self.wfile.flush()

            with _sse_lock:
                _sse_clients.append(sender)

            # Send initial connection event
            self.wfile.write(b"event: connected\ndata: {\"type\":\"connected\"}\n\n")
            self.wfile.flush()

            # Send current history on connect
            with _history_lock:
                items = [{"filename": h["filename"], "title": h["title"], "timestamp": h["timestamp"]} for h in _history]
            history_payload = json.dumps({"type": "history-update", "items": items})
            self.wfile.write(f"event: history-update\ndata: {history_payload}\n\n".encode("utf-8"))
            self.wfile.flush()

            # Keep connection alive, send ping every 25s
            try:
                while True:
                    time.sleep(25)
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
            except Exception:
                with _sse_lock:
                    if sender in _sse_clients:
                        _sse_clients.remove(sender)
            return
        elif self.path == "/artifacts.json":
            # Serve history manifest
            with _history_lock:
                items = [{"filename": h["filename"], "title": h["title"], "timestamp": h["timestamp"]} for h in _history]
            self._send(200, "application/json", json.dumps(items).encode())
        elif self.path.startswith("/history/"):
            # Serve archived artifact file
            filename = self.path[9:]  # Remove "/history/" prefix
            # Security: prevent directory traversal
            filename = os.path.basename(filename)
            filepath = os.path.join(HISTORY_DIR, filename)
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self._send(200, "text/html; charset=utf-8", content)
            else:
                self._send(404, "text/plain", b"Not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/update":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                # Write new content first, then archive (newest appears at top of history)
                with open(ARTIFACT_FILE, "w", encoding="utf-8") as f:
                    f.write(body)
                global _mtime_artifact, _cached_artifact, _cached_etag_artifact
                _mtime_artifact = os.stat(ARTIFACT_FILE).st_mtime
                _cached_artifact = body.encode("utf-8")
                _cached_etag_artifact = hashlib.md5(_cached_artifact).hexdigest()[:16]
                print(f"[{time.strftime('%H:%M:%S')}] Saved artifact ({len(body):,} bytes)")

                # Archive new content to history (after write so newest appears at top)
                _archive_artifact()

                # Broadcast live reload to all connected browsers
                _notify_clients("reload")

                self._send(200, "text/plain", b"OK")
            except Exception as e:
                self._send(500, "text/plain", str(e).encode())
        elif self.path == "/notify-open":
            # Server receives signal to open browser (called by skill after writing artifact)
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
            try:
                data = json.loads(body)
                mode = data.get("mode", "square")
                with _open_lock:
                    _pending_open["mode"] = mode
                print(f"[{time.strftime('%H:%M:%S')}] Browser open requested (mode={mode})")
                self._send(200, "text/plain", b"OK")
            except Exception as e:
                self._send(500, "text/plain", str(e).encode())
        elif self.path == "/share-screenshot":
            # Receive base64 PNG, save to Downloads, open Preview
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            try:
                # Write base64 to temp file for the Python script
                tmpfile = os.path.join(DIRECTORY, ".screenshot_tmp.b64")
                with open(tmpfile, "w") as f:
                    f.write(body)
                # Run the share script
                result = subprocess.run(
                    ["python3", os.path.join(DIRECTORY, "share-screenshot.py")],
                    input=body.encode("utf-8"),
                    capture_output=True, timeout=15
                )
                os.remove(tmpfile)
                print(f"[{time.strftime('%H:%M:%S')}] Screenshot: {result.stdout.decode().strip()}")
                self._send(200, "text/plain", b"OK")
            except subprocess.TimeoutExpired:
                self._send(500, "text/plain", b"Screenshot timeout")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Screenshot error: {e}")
                self._send(500, "text/plain", str(e).encode())
        elif self.path == "/check-open":
            # Browser polls this to know if it should auto-open (for initial load)
            with _open_lock:
                mode = _pending_open["mode"]
            self._send(200, "application/json", json.dumps({"mode": mode}).encode())
        elif self.path == "/clear-open":
            # Browser consumed the open flag
            with _open_lock:
                _pending_open["mode"] = None
            self._send(200, "text/plain", b"OK")
        else:
            self._send(404, "text/plain", b"Not found")

    def _send(self, code, ctype, content):
        if isinstance(content, str):
            content = content.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(content))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(content)

    def log_message(self, format, *args):
        msg = args[0] if args else ""
        if msg and msg not in ("favicon.ico", "GET / HTTP/1.1", "GET /index.html HTTP/1.1"):
            print(f"[{time.strftime('%H:%M:%S')}] {msg}")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def run_server():
    # Load history on startup
    _load_history()
    _archive_artifact()   # Auto-capture initial artifact.html on server start

    server = ThreadedHTTPServer(("", PORT), Handler)
    print(f"Artifact Preview v4.0 server running on http://localhost:{PORT}")
    print(f"  /              → Preview UI")
    print(f"  /artifact      → Raw artifact HTML")
    print(f"  /update        → POST to save artifact + broadcast reload")
    print(f"  /events        → SSE stream for live reload")
    print(f"  /notify-open   → POST to trigger browser open")
    print(f"  /history/<file>→ Serve archived artifacts")
    print(f"  /artifacts.json→ History manifest")
    print(f"\nServing: {DIRECTORY}")
    print(f"History: {len(_history)} items (max {MAX_HISTORY})")
    print("\nPress Ctrl+C to stop\n")

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: (print("\nShutting down..."), server.shutdown()))
    server.serve_forever()


if __name__ == "__main__":
    read_index()
    read_artifact()
    run_server()
