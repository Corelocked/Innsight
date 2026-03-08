import json
from http.server import BaseHTTPRequestHandler

from backend import handle_user_input


class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)
        self.wfile.write(b'')

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(raw_body.decode('utf-8') or '{}')
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid JSON payload'}).encode('utf-8'))
            return

        user_input = str(data.get('input', '')).strip()
        if not user_input:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'No input provided'}).encode('utf-8'))
            return

        if len(user_input) > 1000:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Input too long (max 1000 characters)'}).encode('utf-8'))
            return

        try:
            response = handle_user_input(user_input)
            self._set_headers(200)
            self.wfile.write(json.dumps({'response': response}).encode('utf-8'))
        except Exception as e:
            print(f"Error in voice_order handler: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Internal server error'}).encode('utf-8'))
