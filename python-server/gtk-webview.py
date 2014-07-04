#!/usr/bin/env python

from socketio.server import SocketIOServer
from mdma.socketiogame import SocketApp

from multiprocessing import Process, Queue

from gi.repository import WebKit
from gi.repository import Gtk
from gi.repository import GObject as gobject

def socketio_server(q):
    server = SocketIOServer(('0.0.0.0', 0), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    q.put(port)
    server.serve_forever()

class mywindow(Gtk.Window):
  def __init__(self, url):
    Gtk.Window.__init__(self)
    self.browser = WebKit.WebView()
    self.browser.open(url)
    self.add(self.browser)
    self.show()

  def quit(self,*args):
    self.hide()
    self.destroy()

class App():
  def __init__(self):
    q = Queue()
    self.ioserver = Process(target=socketio_server, args=(q,))
    self.ioserver.start()
    port = q.get()

    gobject.threads_init()
    self.mainloop = gobject.MainLoop()

    url = 'http://google.com'
    url = 'http://localhost:'+str(port)+'//client/index.html'
    win = mywindow(url)
    win.connect("destroy", self.quit)
    win.show_all()

    self.mainloop.run()

  def quit(self, sender):
    print "WHAT"
    self.ioserver.terminate()
    self.mainloop.quit()

if __name__ == '__main__':
    app = App()

