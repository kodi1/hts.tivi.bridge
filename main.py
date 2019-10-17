#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

def cmd_get_dbg():
  return raw_input("q - quit\nr - restart\n")

def main():
    server.my_serv.start()
    try:
        while True:
            c = raw_input("q - quit\nr - restart\n")
            if c:
              print c
            if c == "q":
                break;
            if c == "r":
                server.my_serv.restart()
    except KeyboardInterrupt:
        print "\nKeyboardInterrupt"
        pass

def __log(fmt, data):
    print fmt % data

if __name__ == "__main__":
  mac = os.getenv('TIVIBG_MAC', False)
  if not mac:
    sys.exit('TIVIBG_MAC is not set\nTIVIBG_MAC=aa:bb:cc:dd:ee:ff %s' % (sys.argv[0]))
  import server
  server.log_cb = __log
  server.my_serv = server.serv(host=os.uname()[1])

  main()

  del server.my_serv
