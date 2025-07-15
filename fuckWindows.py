"""
不区分路径大小写的简单 HTTP 服务器
"""
import http.server
import os
import socketserver
import sys
from pathlib import Path

glob = Path(".").glob

class FuckWindows(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = "/" + str(next(glob("index.htm{l,}", case_sensitive=False)))
        else:
            try:
                self.path = "/" + str(next(glob(self.path[1:], case_sensitive=False)))
            except StopIteration:
                pass
        return super().do_GET()

port = 0
try:
    port = int(sys.argv[1])
except IndexError | ValueError:
    print("用法：", sys.argv[0], "<端口>")
if port:
    with socketserver.TCPServer(("", port), FuckWindows) as httpd:
        print(f"serving at port {port}")
        httpd.serve_forever()
