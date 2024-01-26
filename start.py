import argparse
import http.server
import os

# 使用argparse模块来处理命令行参数
parser = argparse.ArgumentParser(description="A simple HTTP server")
parser.add_argument("-p", "--port", type=int, help="The website port")
parser.add_argument("-i", "--id", type=str, help="site id")
args = parser.parse_args()
os.chdir(f"./{args.id}/")


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """处理请求并返回页面"""

    # 处理一个GET请求
    def do_GET(self):
        def httpok(REP=200):
            if "Range" in self.headers:  # 多线程实现
                range_header = self.headers["Range"]
                start = int(range_header.split("=")[1].split("-")[0])
                self.send_response(REP)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", "attachment")
                self.send_header("Content-Range", f"bytes {start}-")
            else:
                self.send_response(REP)
            self.end_headers()
        link = "."+self.path
        if link == "./":link="./index.html"
        if os.path.exists(link) is True:
            httpok()
        else:
            if os.path.isdir(link):
                try:
                    if link[-1]=="/" or link[-1]=="\\":
                        link+="index.html"
                    else:
                        link+="\\index.html"
                except OSError:
                    httpok(404)
                    if os.path.exists("404.html"):
                        link="../404.html"
        print(os.path.abspath(link))
        Page = open(link, mode="rb")
        self.wfile.write(Page.read())
if __name__ == "__main__":
    serverAddress = ("", args.port)  # 端口
    server = http.server.ThreadingHTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
