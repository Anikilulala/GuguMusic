from http.server import *
if __name__ == '__main__':
    port=8123
    bind=""
    protocol="HTTP/1.0"
    server_address = (bind, port)
    HandlerClass=CGIHTTPRequestHandler
    HandlerClass.protocol_version = protocol
    with HTTPServer(server_address, HandlerClass) as httpd:
        httpd.serve_forever()