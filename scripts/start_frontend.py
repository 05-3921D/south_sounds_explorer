import http.server
import socketserver
import os

PORT = 5500
DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "frontend")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    print(f"Starting Frontend Server at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.server_close()
