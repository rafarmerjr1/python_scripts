#Python3 http server for GET and POST request logging to output

import argparse
import textwrap
import logging
import os
from  urllib.parse import unquote
from http.server import HTTPServer, BaseHTTPRequestHandler

class B(BaseHTTPRequestHandler):
    def _set_response(self):       #send back a 200 HTTP response & headers
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        try:
            if str(self.path) == '/':
                self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
                self.list_directory(self.path)
            elif "." in str(self.path):
                try:
                    self.wfile.write(format(self.path).encode('utf-8'))
                    self.wfile.write(b"\n")
                    path = format(self.path)
                    filename = ("."+path)
                    f = open(filename, 'r')
                    self.wfile.write(f.read().encode('utf-8'))
                    self.wfile.write(b"\n")
                    f.close()
                    return
                except:
                    self.wfile.write(b"Cannot locate specified file\n")
                    self.list_directory(self.path)
            else:
                self.wfile.write(b"Error. \n")
                self.wfile.write(b"Try a different filename or directory: \n")
                self.list_directory(self.path)
        except:
                self.wfile.write(b"Failed to access. File or connection issue. \n")

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = unquote(post_data.decode('utf-8')).split("&")
        logging.info("\nPOST request,\nPath: %s\nHeaders:\n%s\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(b"\n")

    def list_directory(self,path):
        self.wfile.write(b"\nAttempting to list current directory:\n")
        try:
            self.wfile.write(b"Your query: \n")
            self.wfile.write((self.path).encode('utf-8'))
            self.wfile.write(b"\n")
            filepath = os.getcwd()
            list = os.listdir(filepath)
            self.wfile.write(b"\nPresent in current directory: \n")
            for item in list:
                self.wfile.write(format(item).encode('utf-8'))
                self.wfile.write(b"\n")
        except:
            self.wfile.write(b"*** Error listing files *** \n")

def run(server_class=HTTPServer, handler_class=B, addr="localhost", port=8000): #Start Server
    logging.basicConfig(level=logging.INFO)
    server_address=(addr, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse. ArgumentParser(
     description ='Small python server to catch and output HTTP requests',
     formatter_class=argparse.RawDescriptionHelpFormatter,
     epilog=textwrap.dedent('''
     Functionality:
     Default without args: 127.0.0.1:8000

     GET requests: Can list files in directory by requesting \'/\'.
     GET requests: Can return text file content as output.
     POST requests: Can accept POST request parameters and output on server terminal.
     python3 http_server_small.py -l <IP> -p <port> #listen on this IP:Port \n
     Send a GET request:
         curl http://localhost:8000
         curl 127.0.0.1:8000
         curl 127.0.0.1:8000/test_file.html
     Send a POST request:
         curl -d "foo=bar&bin=baz" http://localhost:8000
    '''))
    parser.add_argument('-l', '--listen',default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8000)
    args = parser.parse_args()
    print("Starting Server... ... ...")
    print("Listen: %s \nPort: %i\n" % (args.listen, args.port))
    run(addr=args.listen, port=args.port)
