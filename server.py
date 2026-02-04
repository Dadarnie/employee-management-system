#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend on localhost:8000
Run with: python3 server.py
"""

import http.server
import socketserver
import os
import sys

PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✓ Frontend server running on http://localhost:{PORT}")
            print(f"✓ Serving files from: {DIRECTORY}")
            print(f"✓ Backend API: http://localhost:5000/api")
            print(f"\nOpen in browser: http://localhost:{PORT}")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"✗ Port {PORT} is already in use")
            sys.exit(1)
        raise
