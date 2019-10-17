# -*- coding: utf8 -*-
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost:8888
Send a HEAD request::
    curl -I curl http://localhost:8888
Send a POST request::
    curl -d "foo=bar&bin=baz" curl http://localhost:8888
"""

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import threading

import os
import simplejson as json
import tivi

ch_cb = None
log_cb = None
my_serv = None

def my_log (fmt, data):
    if log_cb:
        log_cb(fmt, data)

def reboot(s, arg= None):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><body><h1>restart!</h1></body></html>")

    def rst(arg):
        thr = threading.current_thread()
        arg.restart()
        my_log ("%s Reboot server", thr.getName())

    t = threading.Thread(target=rst, name="Httpd_reboot", kwargs={"arg": my_serv})
    #t.setDaemon(True)
    t.start()

def get_id(s, arg):
    s.send_response(302)
    s.send_header("Content-type", "application/x-mpegurl")

    _url = s.server.tivi.get_ch(arg)
    if not _url:
      _url = 'http://google.bg'

    s.send_header("Location", _url)
    s.end_headers()

def err_responce(s):
    s.send_response(404)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<b<html>ody><h1>Error!</h1></body></html>")
    s.wfile.write("Path:\n%s\nHeader:\n%s" % (s.path, s.headers))

def pls(s):
    _list = s.server.tivi.get_pls()
    s.send_response(200)
    s.send_header("Content-type", "application/x-mpegurl")
    s.end_headers()
    s.wfile.write(_list)

map_cmd = {
    'reboot' : reboot,
    'id': get_id,
    'tivi' : pls,
    }

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      spath = self.path.split("/")
      if len(spath) == 2:
          map_cmd.get(spath[1], err_responce)(self)
          return
      elif len(spath) == 3:
          map_cmd.get(spath[1], err_responce)(self, spath[2])
          return
      err_responce(self)

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, format, *args):
        if ch_cb:
          ch_cb(self.path)
        my_log("%s", self.headers['User-Agent'])
        my_log(format, args)

def worker(serv, stop):
    thr = threading.current_thread()
    while not stop.is_set():
        serv.serve_forever()
        my_log ("%s Exit server", thr.getName())

class myServer(HTTPServer):
    def __init__(self, s, h, b):
        HTTPServer.__init__(self, s, h)
        self.tivi = b

class serv():
    def __init__(self, server="", host='localhost', port=8888, log=None):
        self._port = port
        self._server = myServer((server, self._port), MyHandler, tivi.data(os.getenv('TIVIBG_MAC'), host, port))

    def start (self):
        my_log("%s", "Start server")
        self._stop = threading.Event()
        self._work = threading.Thread(target=worker, name="Httpd", kwargs={"serv": self._server, "stop":  self._stop})
        self._work.start()

    def __stop (self):
        my_log("%s", "Stop server")
        self._stop.set()
        self._server.shutdown()
        self._work.join()

    def restart(self):
        self.__stop ()
        self.start()

    def __del__(self):
        my_log("%s", "Del server")
        self.__stop()
