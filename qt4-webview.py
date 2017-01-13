#!/usr/bin/env python

from gevent import monkey
import gipc
import sys

from PyQt4 import QtGui, QtCore, QtWebKit

from socketio.server import SocketIOServer
from lib.socketiogame import SocketApp


monkey.patch_all()
port = 38478
ioserver = webserver = None


def socketio_server(q):
    server = SocketIOServer(('0.0.0.0', 0), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    q.put(port)
    server.serve_forever()


class MyWindow(QtWebKit.QWebView):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def showSelectFirstDeviceDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/dev')
        print fname

    def showSelectSecondDeviceDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/dev')
        print fname

    def initUI(self):
        self.setWindowTitle("Meditation Deathmatch")

        icon = QtGui.QIcon.fromTheme("open")
        openFirst = QtGui.QAction(icon, 'Select First Device', self)
        openFirst.setShortcut('Ctrl+1')
        openFirst.setStatusTip('Select First Device')
        openFirst.triggered.connect(self.showSelectFirstDeviceDialog)

        icon = QtGui.QIcon.fromTheme("open")
        openSecond = QtGui.QAction(icon, 'Select Second Device', self)
        openSecond.setShortcut('Ctrl+2')
        openSecond.setStatusTip('Select First Device')
        openSecond.triggered.connect(self.showSelectFirstDeviceDialog)

        self.menubar = QtGui.QMenuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(openFirst)
        fileMenu.addAction(openSecond)


def qt_app():
    app = QtGui.QApplication(sys.argv)
    web = MyWindow()
    url = 'http://localhost:'+str(port)+'//client/index.html'
    web.load(QtCore.QUrl(url))
    frame = web.page().mainFrame()
    frame.setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
    web.show()
    web.raise_()
    web.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    ioserver = gipc.start_process(target=socketio_server)
    webview = gipc.start_process(target=qt_app)
