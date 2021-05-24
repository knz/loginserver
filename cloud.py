from sys import argv, exit
from random import randint
import webbrowser
import time
import urllib.request
import os

# this is harcoded in the login command and should point to a secure,
# centralized login form (or HTTP redirector to another system that
# provides the login service).
login_service = "http://192.168.2.10:9000"

# Standard token location.
tokenpath = os.environ["HOME"] + "/.config/cockroachcloud"
tokenfile = "login-token"

from builtins import open as openfunc

def finish_login(response):
    response = response.strip()
    os.makedirs(tokenpath, mode = 0o700, exist_ok = True)
    with openfunc(tokenpath + "/" + tokenfile, "w") as f:
        f.write(response)
    pass

def do_login():
    # generate a unique client identifier.
    # in a real client this would use a UUID.
    client = str(randint(0, 100000))
    loginurl = login_service + "/login/" + client
    didopen = webbrowser.open(loginurl, new=2)
    if not didopen:
        print("""
Could not open a web browser. Please copy-paste
the following URL manually in your web browser
before continuing:

    """, loginurl)

    checkurl = login_service + "/check/" + client
    starttime = time.monotonic()
    while True:
        respbytes = urllib.request.urlopen(checkurl).read()
        response = respbytes.decode('utf-8')
        if response.startswith("ok"):
            # done
            response = response.lstrip("ok")
            print("OK!")
            finish_login(response)
            return True
        curtime = time.monotonic()
        if curtime - starttime > 120:
            print("login lasted too long")
            return False
        # not done yet
        time.sleep(1)

def do_logout():
    pass

# wanted journey:
# import cockroach
# connmgr = cockroach.open() # no args! see below for details
# conn = connmgr.connect() # no args
# from here on the conn object is a regular SQL connection object

class connector(object):
    def __init__(self, url):
        self.url = url

    def connect(self):
        import psycopg2
        return psycopg2.connect(self.url)

def open():
    filename = tokenpath + "/" + tokenfile
    if not os.path.exists(filename):
        raise "token not defined; use 'cloud login' first"
    with openfunc(filename) as f:
        token = f.read().strip()
    server, user, db, pwd = token.split(' ')
    # FIXME: use proper URL encoding here.
    return connector("postgresql://"+user+":"+pwd+"@"+server+"/"+db)


if __name__ == "__main__":
    if len(argv) < 2:
        print("usage:", argv[0]," login|logout")
        exit(0)

    if argv[1] == "login":
        do_login()
    elif argv[1] == "logout":
        response = do_login()
        if response:
            exit(0)
        else:
            exit(1)
    else:
        print("unrecognized command:", argv[1])
