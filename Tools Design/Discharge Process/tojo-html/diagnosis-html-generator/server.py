"""
Tojo HTML service — a tiny HTTP wrapper so any backend (Python, Node, Go …) can hand the
generator Claude's response spec and get the HTML back. Standard library only.

  python3 server.py --port 8080

  POST /render     body: {"spec": {...}, "view": "canvas"|"desktop"|"mobile", "fonts": "embed"|"none"}
                   → 200 {"ok": true,  "html": "...", "chat": {...}, "warnings": [...], "estimate": {...}}
                   → 422 {"ok": false, "errors": [...], "warnings": [...]}   ← send "errors" back to Claude once
  POST /validate   body: {"spec": {...}}  → {"ok": bool, "errors": [...], "warnings": [...]}
  GET  /health     → {"ok": true, "registry_version": N, "blocks": N}

Stateless: every request is independent, so it scales by running more copies.
In a Python backend you can skip HTTP and call diagnosis_html.validate() / diagnosis_html.render_page() directly.
"""
import argparse, json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import diagnosis_html

MAX_BODY = 2 * 1024 * 1024

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == '/health':
            reg = diagnosis_html.load_registry()
            return self._send(200, {'ok': True, 'registry_version': reg.get('registry_version'), 'blocks': len(reg['blocks'])})
        self._send(404, {'ok': False, 'errors': ['not found']})

    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > MAX_BODY:
            return self._send(413, {'ok': False, 'errors': ['body missing or too large']})
        try:
            req = json.loads(self.rfile.read(n).decode('utf-8'))
            spec = req['spec']
        except Exception as ex:
            return self._send(400, {'ok': False, 'errors': ['request must be JSON with a "spec" field: %s' % ex]})
        reg = diagnosis_html.load_registry()          # re-read each time, so registry approvals apply without a restart
        errs, warns = diagnosis_html.validate(spec, reg)
        if self.path == '/validate':
            return self._send(200, {'ok': not errs, 'errors': errs, 'warnings': warns})
        if self.path != '/render':
            return self._send(404, {'ok': False, 'errors': ['not found']})
        if errs:
            return self._send(422, {'ok': False, 'errors': errs, 'warnings': warns})
        view = req.get('view', 'canvas')
        if view not in ('canvas', 'desktop', 'mobile'):
            return self._send(400, {'ok': False, 'errors': ['view must be canvas, desktop or mobile']})
        old = diagnosis_html.FONT_MODE
        diagnosis_html.FONT_MODE = req.get('fonts', old)
        try:
            html_out = diagnosis_html.render_page(spec, view)
        finally:
            diagnosis_html.FONT_MODE = old
        self._send(200, {'ok': True, 'html': html_out, 'chat': spec.get('chat', {}), 'warnings': warns, 'estimate': spec.get('_estimate', {})})

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--port', type=int, default=8080); ap.add_argument('--host', default='127.0.0.1')
    a = ap.parse_args()
    print('Tojo HTML service on http://%s:%d' % (a.host, a.port))
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()
