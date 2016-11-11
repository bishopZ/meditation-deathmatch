#!/usr/bin/env python

import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QAction, QMenuBar
from PyQt5.QtWebKitWidgets import QWebView

from socketio.server import SocketIOServer
from lib.socketiogame import SocketApp

from multiprocessing import Process, Queue

import gevent


def socketio_server(q):
    server = SocketIOServer(('0.0.0.0', 0), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    q.put(port)
    server.serve_forever()


class PyQtGreenlet(gevent.Greenlet):
    def __init__(self, app):
        gevent.Greenlet.__init__(self)
        self.app = app

    def _run(self):
        while True:
            self.app.processEvents()
            while self.app.hasPendingEvents():
                self.app.processEvents()
                gevent.sleep(0.01)
        gevent.sleep(0.01)


class MyWindow(QWebView):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def showSelectFirstDeviceDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/dev')
        print(fname)

    def showSelectSecondDeviceDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/dev')
        print(fname)

    def initUI(self):
        self.setWindowTitle("Meditation Deathmatch")
        icon = QtGui.QIcon.fromTheme("open")
        openFirst = QAction(icon, 'Select First Device', self)
        openFirst.setShortcut('Ctrl+1')
        openFirst.setStatusTip('Select First Device')
        openFirst.triggered.connect(self.showSelectFirstDeviceDialog)

        icon = QtGui.QIcon.fromTheme("open")
        openSecond = QAction(icon, 'Select Second Device', self)
        openSecond.setShortcut('Ctrl+2')
        openSecond.setStatusTip('Select First Device')
        openSecond.triggered.connect(self.showSelectFirstDeviceDialog)

        self.menubar = QMenuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(openFirst)
        fileMenu.addAction(openSecond)

if __name__ == '__main__':
    q = Queue()
    ioserver = Process(target=socketio_server, args=(q,))
    f = gevent.spawn(ioserver.start())
    port = q.get()
    url = 'http://localhost:'+str(port)+'//client/index.html'

    app = QApplication(sys.argv)
    web = MyWindow()
    web.load(QtCore.QUrl(url))

    web.page().mainFrame().setScrollBarPolicy(
        QtCore.Qt.Vertical,
        QtCore.Qt.ScrollBarAlwaysOff)

    web.show()
    web.raise_()
    web.showFullScreen()

    g = PyQtGreenlet.spawn(app)
    gevent.joinall([f, g])
