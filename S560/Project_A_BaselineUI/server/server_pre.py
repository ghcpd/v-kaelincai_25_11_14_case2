#!/usr/bin/env python3
import http.server
import socketserver
import os

HOST='127.0.0.1'
PORT=8000
ROOT_DIR=os.path.join(os.path.dirname(__file__),'..','src')

os.chdir(ROOT_DIR)
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving {ROOT_DIR} at http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Stopped')
