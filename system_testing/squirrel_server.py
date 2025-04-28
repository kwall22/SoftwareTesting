import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from squirrel_db import SquirrelDB

class SquirrelServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        resourceName, resourceId = self.parsePath()
        if resourceName == "squirrels":
            if resourceId:
                self.handleSquirrelsRetrieve(resourceId)
            else:
                self.handleSquirrelsIndex()
        else:
            self.handle404()

    def do_POST(self):
        resourceName, resourceId = self.parsePath()
        if resourceName == "squirrels":
            if resourceId:
                self.handle404()
            else:
                self.handleSquirrelsCreate()
        else:
            self.handle404()

    def do_PUT(self):
        resourceName, resourceId = self.parsePath()
        if resourceName == "squirrels":
            if resourceId:
                self.handleSquirrelsUpdate(resourceId)
            else:
                self.handle404()
        else:
            self.handle404()

    def do_DELETE(self):
        resourceName, resourceId = self.parsePath()
        if resourceName == "squirrels":
            if resourceId:
                self.handleSquirrelsDelete(resourceId)
            else:
                self.handle404()
        else:
            self.handle404()

    def getRequestData(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        for key in data:
            data[key] = data[key][0]
        return data

    def parsePath(self):
        if self.path.startswith("/"):
            parts = self.path[1:].split("/")
            resourceName = parts[0]
            resourceId = None
            if len(parts) > 1:
                resourceId = parts[1]
            return (resourceName, resourceId)
        return False

    def handleSquirrelsIndex(self):
        db = SquirrelDB()
        squirrelsList = db.getSquirrels()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(squirrelsList), "utf-8"))

    def handleSquirrelsRetrieve(self, squirrelId): 
        db = SquirrelDB()
        squirrel = db.getSquirrel(squirrelId)
        if squirrel:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(squirrel), "utf-8"))
        else:
            self.handle404()

    def handleSquirrelsCreate(self):  
        db = SquirrelDB()
        body = self.getRequestData()
        db.createSquirrel(body["name"], body["size"])
        self.send_response(201)
        self.end_headers()

    def handleSquirrelsUpdate(self, squirrelId):  
        db = SquirrelDB()
        squirrel = db.getSquirrel(squirrelId)
        if squirrel:
            body = self.getRequestData()
            db.updateSquirrel(squirrelId, body["name"], body["size"])
            self.send_response(204)
            self.end_headers()
        else:
            self.handle404()

    def handleSquirrelsDelete(self, squirrelId): 
        db = SquirrelDB()
        squirrel = db.getSquirrel(squirrelId)
        if squirrel:
            db.deleteSquirrel(squirrelId)
            self.send_response(204)
            self.end_headers()
        else:
            self.handle404()

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("404 Not Found", "utf-8"))

def run():
    print("squirrel server running at 127.0.0.1:8080")
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, SquirrelServerHandler)
    server.serve_forever()

if __name__ == '__main__':
    run()