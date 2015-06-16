#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore, QtWebKit


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

        openFirst = QtGui.QAction(QtGui.QIcon.fromTheme("open"), 'Select First Device', self)
        openFirst.setShortcut('Ctrl+1')
        openFirst.setStatusTip('Select First Device')
        openFirst.triggered.connect(self.showSelectFirstDeviceDialog)

        openSecond = QtGui.QAction(QtGui.QIcon.fromTheme("open"), 'Select Second Device', self)
        openSecond.setShortcut('Ctrl+2')
        openSecond.setStatusTip('Select First Device')
        openSecond.triggered.connect(self.showSelectFirstDeviceDialog)

        self.menubar = QtGui.QMenuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(openFirst)
        fileMenu.addAction(openSecond)


if __name__ == '__main__':
    port = 3101
    url = 'http://localhost:'+str(port)+'//client/index.html'

    app = QtGui.QApplication(sys.argv)
    web = MyWindow()
    web.load(QtCore.QUrl(url))

    web.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

    web.show()
    web.raise_()
    web.showFullScreen()

    app.exec_()
