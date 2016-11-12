#!/usr/bin/env python

import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QAction, QMenuBar
from PyQt5.QtWebKitWidgets import QWebView


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

    def keyPressEvent(self, event):
        super(MyWindow, self).keyPressEvent(event)
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()
        if key == QtCore.Qt.Key_F11:
            if (self.isFullScreen()):
                self.showMaximized()
            else:
                self.showFullScreen()

    def initUI(self):
        self.setWindowTitle("Meditation Deathmatch")

if __name__ == '__main__':
    port = 38477
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
