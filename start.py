"使用的模块:";import argparse as a_p;import http.server as h_s;import os as o;"使用argparse模块来处理参数:";paser = a_p.ArgumentParser(description="A simple HTTP server");paser.add_argument("-p", "--port", type=int, help="The website port"),paser.add_argument("-i", "--id", type=str, help="site id");args = paser.parse_args();"<--|-->";o.chdir(f"./{args.id}/")
class RequestHandler(h_s.BaseHTTPRequestHandler):
    def do_GET(self):
        "返回页面";o_p=o.path;lnk = "."+self.path#初事化
        def httpok(R=200):
            s_h,s_r,s_e=self.send_header,self.send_response,self.end_headers
            if "Range" in self.headers: 
                "多线程下载实现:";s_t=int(self.headers["Range"].split("=")[1].split("-")[0]);s_r(R)
                for header in [("Content-Type", "application/octet-stream"),("Content-Disposition", "attachment"),("Content-Range", f"bytes {s_t}-")]:s_h(header)
            else:s_r(R)
            s_e()
        if lnk == f"./":lnk = f"./index.html"
        if o_p.exists(lnk) is True:httpok()
        else:
            if o_p.isdir(lnk):lnk += "index.html"if lnk[-1] == "/" or lnk[-1] == "\\"else"\\index.html";"←--如果是文件夹就重定向到里面的index.html"
            if o_p.exists(lnk) is False:lnk = ("./404.html")if o_p.exists("./404.html") else(f"../404.html"),httpok(404);"←--如果页面不存在,就重定向到404页面,如果没有,就用默认的404页面.然后返回404响应"
        print(o_p.abspath(lnk)),self.wfile.write(open(lnk, mode="rb").read()) ;"←--输出文件的绝对路径,然后发送页面"
if __name__ == "__main__":h_s.ThreadingHTTPServer(("", args.port), RequestHandler).serve_forever()