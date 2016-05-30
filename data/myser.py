import BaseHTTPServer
import time
from ajson import data
from json import dumps
import routeconf

HOST_NAME = 'example.net' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.
tag=1 #normal is on

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        if self.path.endswith('json'):
                self.send_header("Content-type", "application/json")
        self.end_headers()
    def do_POST(self):
        MyHandler.do_GET(self)
    def do_GET(self):
        global tag
        """Respond to a GET request."""
        MyHandler.do_HEAD(self)
        if self.path.endswith('json'):
                data['tag']=tag
                self.wfile.write(dumps(data))
        if self.path.endswith('normal'):
                if tag != 1:
                        tag = 1
                        routeconf.normal()
        if self.path.endswith('linkdown'):
                if tag != 0:
                        tag = 0
                        routeconf.linkdown()




if __name__ == '__main__':
    routeconf.normal()
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
