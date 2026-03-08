import json
from http.server import BaseHTTPRequestHandler


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

        user_feedback = str(data.get('feedback', '')).strip()
        if not user_feedback:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'No feedback provided'}).encode('utf-8'))
            return

        if len(user_feedback) > 2000:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Feedback too long (max 2000 characters)'}).encode('utf-8'))
            return

        print(f"Feedback received: {user_feedback[:100]}...")
        self._set_headers(200)
        self.wfile.write(json.dumps({'message': 'Thank you for your feedback!'}).encode('utf-8'))
