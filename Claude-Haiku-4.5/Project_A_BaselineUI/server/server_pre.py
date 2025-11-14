from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import threading
import time

class TaskListServer:
    def __init__(self, port=8080, directory=None):
        self.port = port
        self.directory = directory or os.path.join(os.path.dirname(__file__), '..', 'src')
        self.server = None
        self.thread = None
        
    def start(self):
        """Start the HTTP server in a separate thread"""
        os.chdir(self.directory)
        
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                # Suppress default logging
                pass
                
        self.server = HTTPServer(('localhost', self.port), QuietHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        # Wait a moment for server to start
        time.sleep(1)
        print(f"Baseline UI server started at http://localhost:{self.port}")
        
    def stop(self):
        """Stop the HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Baseline UI server stopped")

if __name__ == "__main__":
    server = TaskListServer()
    try:
        server.start()
        print("Press Ctrl+C to stop the server")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        sys.exit(0)