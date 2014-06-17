#!/usr/bin/env python

import sys
import pexpect 

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class gameServer(QThread):

  def __init__(self, parent, stopSignal):
    QThread.__init__(self, parent=app)
    self.sig1 = SIGNAL("sig1")
    self.stopSignal = stopSignal
    self.parent = parent
    self.abort = False
    self.connect(self.parent, self.stopSignal, self.catchOne)

  def catchOne(self, msg):
    self.abort = True
    self.child.close()

  def run(self):
    self.abort = False
    self.child = pexpect.spawn("./server.py")
    ret = self.child.expect("Listening on port")
    self.emit(self.sig1, "ready")
    while (not self.abort):
      try:
        line = self.child.readline()
      except:
        line = False
      if line:
        print line.rstrip()

class MyWebView(QWebView):

  def __init__(self):
    super(MyWebView, self).__init__(None)
    QTimer.singleShot(0, self.startServer)

  def startServer(self):
    self.stopServerSignal = SIGNAL("stop server")
    self.serverThread = gameServer(self, self.stopServerSignal)
    self.connect(self.serverThread, self.serverThread.sig1, self.markServerReady)
    self.serverThread.start()

  def markServerReady(self, str):
    self.load(QUrl("http://localhost:8080/client/index.html"))

  def closeEvent(self, event):
    self.emit(self.stopServerSignal, "stop that server")
    self.serverThread.wait()
    event.accept()

app = QApplication(sys.argv)
web = MyWebView()
web.show()
web.raise_()
#web.showFullScreen()
sys.exit(app.exec_())
