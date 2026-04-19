#!/usr/bin/env python3
"""
Artifact Preview Server v4.0 — Fast caching HTTP server with SSE for live updates + history.
Routes:
  /              → UI wrapper (index.html)
  /artifact      → raw artifact HTML content (served as-is)
  /update        → POST to save updated artifact HTML
  /events        → SSE stream for live reload signals + history-update
  /notify-open   → POST to trigger browser auto-open
  /history/<filename> → serve archived artifact
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
HISTORY_DIR = os.path.join(DIRECTORY, "history")
ARTIFACTS_JSON = os.path.join(DIRECTORY, "artifacts.json")
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

# History manifest
_history = []
_history_lock = threading.Lock()


def _extract_title(html_content):
    """Extract readable title from HTML for history labeling."""
    m = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if m:
        return m.group(1).strip()[:60]
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if m:
        return m.group(1).strip()[:60]
    return "Untitled"


def _slugify(title):
    """Convert title to a URL-safe slug."""
    s = re.sub(r'[^\w\s-]', '', title).strip().lower()
    s = re.sub(r'[-\s]+', '-', s)
    return s[:40]


def _load_history():
    """Load history manifest from disk."""
    global _history
    if os.path.exists(ARTIFACTS_JSON):
        try:
            with open(ARTIFACTS_JSON, 'r', encoding='utf-8') as f:
                _history = json.load(f)
        except Exception:
            _history = []


def _save_history():
    """Persist history manifest to disk."""
    with open(ARTIFACTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(_history, f, indent=2)


def _archive_artifact(html_content):
    """Archive current artifact.html to history/ with timestamped name. Returns entry dict."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    ts = time.strftime('%Y%m%d-%H%M%S')
    title = _extract_title(html_content)
    slug = _slugify(title)
    filename = f"{ts}-{slug}.html"
    filepath = os.path.join(HISTORY_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    entry = {
        "filename": filename,
        "title": title,
        "timestamp": time.time(),
        "size": len(html_content.encode('utf-8'))
    }

    with _history_lock:
        _history.insert(0, entry)
        # Prune to MAX_HISTORY
        if len(_history) > MAX_HISTORY:
            pruned = _history[MAX_HISTORY:]
            _history = _history[:MAX_HISTORY]
            for item in pruned:
                path = os.path.join(HISTORY_DIR, item['filename'])
                try:
                    os.remove(path)
                except Exception:
                    pass

    _save_history()
    return entry


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
        elif self.path.startswith("/history/"):
            # Serve archived artifact file
            filename = self.path[9:]  # strip "/history/"
            safe_path = os.path.normpath(os.path.join(HISTORY_DIR, filename))
            if not safe_path.startswith(HISTORY_DIR) or not os.path.exists(safe_path):
                self._send(404, "text/plain", b"Not found")
                return
            with open(safe_path, "r", encoding="utf-8") as f:
                content = f.read().encode("utf-8")
            self._send(200, "text/html; charset=utf-8", content)
            return
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/update":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                # Archive old artifact.html before overwriting
                if os.path.exists(ARTIFACT_FILE):
                    with open(ARTIFACT_FILE, "r", encoding="utf-8") as f:
                        old_content = f.read()
                    if old_content.strip():
                        _archive_artifact(old_content)

                with open(ARTIFACT_FILE, "w", encoding="utf-8") as f:
                    f.write(body)
                global _mtime_artifact, _cached_artifact, _cached_etag_artifact
                _mtime_artifact = os.stat(ARTIFACT_FILE).st_mtime
                _cached_artifact = body.encode("utf-8")
                _cached_etag_artifact = hashlib.md5(_cached_artifact).hexdigest()[:16]
                print(f"[{time.strftime('%H:%M:%S')}] Saved artifact ({len(body):,} bytes)")

                # Broadcast live reload to all connected browsers
                _notify_clients("reload")

                # Broadcast history-update so dropdown refreshes
                with _history_lock:
                    _notify_clients("history-update", {"items": list(_history)})

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
    _load_history()
    server = ThreadedHTTPServer(("", PORT), Handler)
    print(f"Artifact Preview v4.0 server running on http://localhost:{PORT}")
    print(f"  /              → Preview UI")
    print(f"  /artifact      → Raw artifact HTML")
    print(f"  /update        → POST to save artifact + broadcast reload")
    print(f"  /events        → SSE stream (reload + history-update)")
    print(f"  /notify-open   → POST to trigger browser open")
    print(f"  /history/<filename> → serve archived artifact")
    print(f"\nServing: {DIRECTORY}")
    print(f"History: {len(_history)} items (max {MAX_HISTORY})")
    print("Press Ctrl+C to stop\n")

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: (print("\nShutting down..."), server.shutdown()))
    server.serve_forever()


if __name__ == "__main__":
    read_index()
    read_artifact()
    run_server()
