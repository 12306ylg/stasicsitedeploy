import ctypes
import http.server as server
import json
import random
import socket
import sys
import time
from urllib.parse import urlparse as parse
import requests
import os
import xml.etree.ElementTree as et
from threading import *
def _process_deploy_html(deploy_html: str, deployinfo):
    deployhtml = et.parse(deploy_html)
    deployhtml_body = deployhtml.getroot()
    deploy_button = deployhtml_body.find("a")
    deploy_button.set("href", f"http://localhost/{deployinfo.url}")
    temp_html = open(deployinfo.id+".htm", "xb")
    deployhtml.write(temp_html, "utf-8")
    temp_html = open(deployinfo.id+".htm", "a")
    temp_html.write(f"<iframe src=\"{deployinfo.url}\" style=\"bottom: auto;\">json preview</iframe>")
    temp_html = open(deployinfo.id+".htm", "rb")
    return temp_html.read()
def _process_mana_html(siteitem:list,template:open):
    mana_html=et.parse(template)
    item=mana_html.getroot()
    class sitem:
        name=item.find("a")
        id=item.find("id")
        date=item.find("date")
        start=item.find("button").find("a")
    sitem.name.text=siteitem[1]
    sitem.name.set("href",siteitem[2])
    sitem.id.text=siteitem[0]
    sitem.date.text=siteitem[3]
    sitem.start.set("href",f"http://localhost/start?{sitem.id.text}")
    temp=open(f"{sitem.id.text}.tmp","xb")
    mana_html.write(temp)
    temp=open(f"{sitem.id.text}.tmp","r")
    managersite=temp.read()
    temp_name=temp.name
    temp=None
    os.system(f"del {temp_name}")
    print(managersite)
    return managersite
def _site_start(id):
    sock = socket.socket()
    sock.bind(('', 0))
    ip, port = sock.getsockname()
    sock.close()
    print(port,end=" ")
    os.popen(f"start python start.py -p {port} -i {id}")
    print("ok")
    return str(port) , id
class reqhaner(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=UTF-8")
        self.end_headers()
        path = parse(self.path).path
        if self.path == "/favicon.ico":
            return
        if path == "/deploy":
            deploylink = self.path
            deployjson = parse(deploylink).query
            print(deployjson)
            deployinfo = json.loads(requests.get(deployjson).text)

            class deploy:
                name = deployinfo["name"]
                id = deployinfo["id"]
                url = deployjson

            deploy_html = _process_deploy_html(open("deploy.html"), deploy)
            self.wfile.write(deploy_html)
            os.system(f"del {deploy.id}.htm")
        elif self.path == "/":
            class manager:
                list=[]
                site=""
            for info in open("deployed.list").readlines():
                infolist=info.split(" ")
                manager.list.append([infolist[1],infolist[0],infolist[2],infolist[3]])
            for thesite in manager.list:
                manager.site+=_process_mana_html(thesite,open("mana.html"))
            self.wfile.write(manager.site.encode())
        elif path == "/start":
            
            #self.wfile.write(f"<h1>fail</h1><br>id:{start[1]}".encode())
            start=_site_start(parse(self.path).query)
            self.wfile.write(f"<h1>sucess!</h1>at: http://localhost:{start[0]} <br>id:{start[1]}".encode())
        elif self.path != "/":
            deployinfo = json.loads(requests.get(self.path[1:]).text)
            class deploy:
                name = deployinfo["name"]
                id = deployinfo["id"]
                url = deployinfo["url"]
            clone_return=os.system(f"git clone {deploy.url} ./{deploy.id}")
            if clone_return == 0:
                self.wfile.write(f"sucess {os.getcwd()}/{deploy.id}".encode())
                open("deployed.list","a+").write(f"{deploy.name} {deploy.id} {deploy.url} {time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) }\n")
            else:
                self.wfile.write(f"fail {os.getcwd()}/{deploy.id} return:{clone_return}".encode())
Hserver = server.ThreadingHTTPServer(("", 80), reqhaner)
Hserver.serve_forever()
