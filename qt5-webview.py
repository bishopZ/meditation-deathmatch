#!/usr/bin/env python

from gevent import monkey
import gevent
import gipc
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView

from socketio.server import SocketIOServer
from lib.socketiogame import SocketApp


monkey.patch_all()

port = 38478
ioserver = webserver = None

def socketio_server():
    server = SocketIOServer(
        ('0.0.0.0', port),
        SocketApp(),
        policy_server=False)
    server.start()
    server.serve_forever()


def qt_app():
    url = 'http://localhost:'+str(port)+'//client/index.html'
    app = QApplication(sys.argv)
    web = MyWindow()
    web.load(QtCore.QUrl(url))

    web.page().mainFrame().setScrollBarPolicy(
        QtCore.Qt.Vertical,
        QtCore.Qt.ScrollBarAlwaysOff)

    web.show()
    web.raise_()
    geom = QApplication.desktop().screenGeometry()
    web.showFullScreen()
    web.resize(geom.width(), geom.height())
    sys.exit(app.exec_())


class MyWindow(QWebView):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def keyPressEvent(self, event):
        print("key pressed")
        super(MyWindow, self).keyPressEvent(event)
        key = event.key()
        alt_pressed = (event.modifiers() & QtCore.Qt.AltModifier)
        if event.key() == QtCore.Qt.Key_F4 and alt_pressed:
            ioserver.terminate()
            self.close()
        if key == QtCore.Qt.Key_Escape:
            ioserver.terminate()
            self.close()
        if key == QtCore.Qt.Key_F11:
            if (self.isFullScreen()):
                self.showMaximized()
            else:
                self.showFullScreen()

    def initUI(self):
        self.setWindowTitle("Meditation Deathmatch")

if __name__ == '__main__':
    ioserver = gipc.start_process(target=socketio_server)
    webview = gipc.start_process(target=qt_app)
