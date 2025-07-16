"""不区分路径大小写的简单 HTTP 服务器"""

import sys
from http.server import SimpleHTTPRequestHandler
from os.path import abspath
from pathlib import Path
from socketserver import TCPServer
from typing import override

glob = Path(".").glob


class FuckWindows(SimpleHTTPRequestHandler):
    @override
    def do_GET(self):
        try:
            self.path: str = "/" + str(
                next(
                    glob(
                        abspath(self.path)[1:] or "index.htm{l,}", case_sensitive=False
                    )
                )
            )
        except StopIteration:
            pass
        return super().do_GET()


port = 0
try:
    port = int(sys.argv[1])
except IndexError | ValueError:
    print("用法：", sys.argv[0], "<端口>")
if port:
    with TCPServer(("", port), FuckWindows) as httpd:
        print(f"serving at port {port}")
        httpd.serve_forever()
