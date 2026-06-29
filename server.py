import sys
import json
import time
import threading
import serial
import serial.tools.list_ports
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import os

HOST = "127.0.0.1"
PORT = 8765
BAUD = 9600

def resource_path(name):
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.append(os.path.join(getattr(sys, "_MEIPASS", ""), name))
        candidates.append(os.path.join(os.path.dirname(sys.executable), name))
    candidates.append(os.path.join(os.path.dirname(__file__), name))

    for path in candidates:
        if path and os.path.exists(path):
            return path
    return candidates[-1]

STATIC = resource_path("static")

latest = {"angle": 0, "distance": 200}
data_lock = threading.Lock()
ser = None
ser_lock = threading.Lock()
shutdown = threading.Event()

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
}

class Pool(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/stream":
            return self._sse()
        if self.path == "/api/ports":
            return self._ports()
        if self.path in ("/", "/index.html"):
            return self._file("index.html", "text/html; charset=utf-8")
        self._file(self.path.lstrip("/"))

    def do_POST(self):
        if self.path == "/api/serial":
            return self._serial_ctrl()
        if self.path == "/api/command":
            return self._command()

    def _sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        old = ""
        try:
            while not shutdown.is_set():
                with data_lock:
                    cur = json.dumps(latest)
                if cur != old:
                    self.wfile.write(f"data: {cur}\n\n".encode())
                    self.wfile.flush()
                    old = cur
                time.sleep(0.016)
        except Exception:
            pass

    def _ports(self):
        pp = [{"port": p.device, "desc": p.description or p.device}
              for p in serial.tools.list_ports.comports()]
        self._json(pp)

    def _serial_ctrl(self):
        body = self._read_body()
        action = body.get("action")
        ok = False
        if action == "open":
            name = body.get("port", "")
            ok = self._ser_open(name)
        elif action == "close":
            ok = self._ser_close()
            with data_lock:
                latest["angle"] = 0
                latest["distance"] = 200
        self._json({"ok": ok})

    def _command(self):
        body = self._read_body()
        typ = body.get("type", "")
        val = body.get("value", "")
        with ser_lock:
            if ser and ser.is_open:
                ser.write(f"{typ}:{val}\n".encode())
                self._json({"ok": True})
                return
        self._json({"ok": False}, 400)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _file(self, name, ctype=None):
        fp = os.path.join(STATIC, name)
        if not os.path.isfile(fp):
            self.send_response(404)
            self.end_headers()
            return
        if not ctype:
            ctype = MIME.get(os.path.splitext(name)[1], "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with open(fp, "rb") as f:
            self.wfile.write(f.read())

    def _ser_open(self, name):
        global ser
        with ser_lock:
            try:
                if ser and ser.is_open:
                    ser.close()
                ser = serial.Serial(name, BAUD, timeout=0.1)
                return True
            except Exception:
                return False

    def _ser_close(self):
        global ser
        with ser_lock:
            try:
                if ser and ser.is_open:
                    ser.close()
                ser = None
                return True
            except Exception:
                return False


def serial_loop():
    while not shutdown.is_set():
        with ser_lock:
            s = ser
        if s and s.is_open:
            try:
                if s.in_waiting:
                    line = s.readline().decode("utf-8", errors="replace").strip()
                    if "," in line:
                        parts = line.split(",")
                        a, d = int(parts[0]), int(parts[1])
                        with data_lock:
                            latest["angle"] = a
                            latest["distance"] = d
            except Exception:
                pass
        time.sleep(0.005)


if __name__ == "__main__":
    pool = Pool((HOST, PORT), Handler)
    t = threading.Thread(target=serial_loop, daemon=True)
    t.start()
    print(f"\n  http://{HOST}:{PORT}")
    import webbrowser
    webbrowser.open(f"http://{HOST}:{PORT}")
    try:
        pool.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        shutdown.set()
        with ser_lock:
            if ser and ser.is_open:
                ser.close()
        pool.shutdown()
