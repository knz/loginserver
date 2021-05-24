from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse, parse_qs

clients = {}

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/check"):
            client = self.path[6:]
            client = client.lstrip("/")
            result = clients.get(client, False)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if result:
                # token contains:
                # server address
                # sql username
                # input database
                # login credential (fixed password in this example)
                token = "192.168.2.10:26257 demo defaultdb secretpassword"
                self.wfile.write(("ok " + token+"\n").encode('utf-8'))
            else:
                self.wfile.write(("login flow not complete\n").encode('utf-8'))

        elif self.path.startswith("/login"):
            client = self.path[6:]
            client = client.lstrip("/")
            clients[client] = False

        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_response()
            self.wfile.write(("""
<html>
<body>
<h1>Hello!</h1>
Are you a real user? please be honest?
<br/>
<form action=/yesitsme method=get>
  <input type="hidden" name="client" value='"""+str(client)+"""'>
  <label for="fname">Who are you?</label>
  <input type="text" id="name" name="name">
  <input type="submit" value="Log in!">
</form>
<br/>
<small>(This page would be replaced by a real login flow once implemented.)</small>
</body></html>""").encode('utf-8'))

        elif self.path.startswith("/yesitsme"):
            query = urlparse(self.path).query
            fields = parse_qs(query)
            client = fields['client'][0]
            name = fields['name'][0]
            clients[client] = True

        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_response()
            self.wfile.write(("""
<html>
<body>
<h1>Welcome """+str(name)+"""!</h1>

Your login command will automatically complete the login flow from here.
You can close this browser window.
</body></html>""").encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=9000):
    #logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

