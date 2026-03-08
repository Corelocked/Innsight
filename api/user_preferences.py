import json
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=401):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)
        self.wfile.write(b'')

    def do_GET(self):
        self._set_headers(401)
        self.wfile.write(json.dumps({'error': 'Authentication not implemented'}).encode('utf-8'))

    def do_POST(self):
        self._set_headers(401)
        self.wfile.write(json.dumps({'error': 'Authentication not implemented'}).encode('utf-8'))
