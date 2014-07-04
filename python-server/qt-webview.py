#!/usr/bin/env python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from socketio.server import SocketIOServer
from mdma.socketiogame import SocketApp

from multiprocessing import Process, Queue

def socketio_server(q):
    server = SocketIOServer(('0.0.0.0', 0), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    q.put(port)
    server.serve_forever()

if __name__ == '__main__':
  q = Queue()
  ioserver = Process(target=socketio_server, args=(q,))
  ioserver.start()
  port = q.get()
  url = 'http://localhost:'+str(port)+'//client/index.html'
  app = QApplication(sys.argv)
  web = QWebView()
  web.load(QUrl(url))
  web.show()
  sys.exit(app.exec_())