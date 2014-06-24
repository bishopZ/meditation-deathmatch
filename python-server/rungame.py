#!/usr/bin/env python

from PyQt4 import Qt, QtCore, QtGui
import qtgevent
qtgevent.install()
import gevent
from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from pymindwave import headset
from pymindwave.pyeeg import bin_power

import sys, time
import pexpect 

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class GameNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    hs1 = {}
    hs2 = {}
    connected = False
    loop_greenlet = ''

    def raw_to_spectrum(self, rawdata):
        flen = 50
        spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
        return spectrum

    def my_loop(self):
        while True:
            if (self.connected):
                print "fire!"
                t = time.time()
                #print 'attention {0}, meditation {1}'.format(self.hs.get('attention'), self.hs.get('meditation'))
                #print 'alpha_waves {0}'.format(self.hs.get('alpha_waves'))
                #print 'blink_strength {0}'.format(self.hs.get('blink_strength'))
                #print 'raw data:'
                #print self.hs.get('rawdata')
                waves_vector = self.hs1.get('waves_vector')
                meditation = self.hs1.get('meditation')
                attention = self.hs1.get('attention')
                poor_signal = self.hs1.get('poor_signal')
                print 'poor_signal {0}'.format(poor_signal)
                spectrum = self.raw_to_spectrum(self.hs1.get('rawdata')).tolist()
                packet1 = {
                  'timestamp': t,
                  'raw_spectrum': spectrum,
                  'eSense': {
                    'meditation': meditation,
                    'attention': attention,
                  },
                  'eegPower' : {
                    'delta': waves_vector[0],
                    'theta': waves_vector[1],
                    'lowAlpha': waves_vector[2],
                    'highAlpha': waves_vector[3],
                    'lowBeta': waves_vector[4],
                    'highBeta': waves_vector[5],
                    'lowGamma': waves_vector[6],
                    'highGamma': waves_vector[7]
                  },
                  'poorSignalLevel': poor_signal
                }
                waves_vector = self.hs2.get('waves_vector')
                meditation = self.hs2.get('meditation')
                attention = self.hs2.get('attention')
                poor_signal = self.hs2.get('poor_signal')
                spectrum = self.raw_to_spectrum(self.hs2.get('rawdata')).tolist()
                packet2 = {
                  'timestamp': t,
                  'raw_spectrum': spectrum,
                  'eSense': {
                    'meditation': meditation,
                    'attention': attention,
                  },
                  'eegPower' : {
                    'delta': waves_vector[0],
                    'theta': waves_vector[1],
                    'lowAlpha': waves_vector[2],
                    'highAlpha': waves_vector[3],
                    'lowBeta': waves_vector[4],
                    'highBeta': waves_vector[5],
                    'lowGamma': waves_vector[6],
                    'highGamma': waves_vector[7]
                  },
                  'poorSignalLevel': poor_signal
                }
                packets = [packet1, packet2]
                self.emit('mindEvent', packets)
            gevent.sleep(1)
    
    def disconnect_hs(self):
        if (self.connected):
            self.hs1.disconnect()
            self.hs2.disconnect()
            self.hs1.dongle_fs.close()
            self.hs2.dongle_fs.close()
            self.connected = False

    def connect_hs(self):
        self.hs1 = headset.Headset('/dev/tty.MindWaveMobile-DevA-1')
        self.hs2 = headset.Headset('/dev/tty.MindWaveMobile-DevA')
        self.hs1.disconnect()
        self.hs2.disconnect()
        settings1 = self.hs1.dongle_fs.getSettingsDict()
        settings2 = self.hs2.dongle_fs.getSettingsDict()
        for i in xrange(2):
            settings1['rtscts'] = not settings1['rtscts']
            settings2['rtscts'] = not settings2['rtscts']
            self.hs1.dongle_fs.applySettingsDict(settings1)
            self.hs2.dongle_fs.applySettingsDict(settings2)
        gevent.sleep(2)
        self.hs1.connect()
        self.hs2.connect()
  
        while self.hs1.get_state() != 'connected':
            gevent.sleep(1)
            print 'current state hs1: {0}'.format(self.hs1.get_state())
        print 'hs1 connected'
  
        while self.hs2.get_state() != 'connected':
            gevent.sleep(1)
            print 'current state hs2: {0}'.format(self.hs2.get_state())
        print 'hs2 connected'
  
        self.connected = True 
        print 'now connected!'

    def on_request_connect(self):
        print "will connect"
        gevent.Greenlet.spawn(self.connect_hs)
        self.loop_greenlet = gevent.Greenlet.spawn(self.my_loop)

    def on_request_disconnect(self):
        print "will disconnect"
        if ('kill' in dir(self.loop_greenlet)):
          self.loop_greenlet.kill()
        self.disconnect_hs()

class SocketApp(object):
    def __init__(self):
        self.buffer = []
        # Dummy request object to maintain state between Namespace
        # initialization.
        self.request = {
            'nicknames': [],
        }

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ['<h1>Welcome. '
                'Try the <a href="/chat.html">chat</a> example.</h1>']

        if path.startswith('client/') or path == 'chat.html':
            try:
                data = open(path).read()
            except Exception:
                return self.not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'': GameNamespace}, self.request)
        else:
            return self.not_found(start_response)

    def not_found(start_response):
        start_response('404 Not Found', [])
        return ['<h1>Not Found</h1>']


class MyWebView(QWebView):

  def __init__(self):
    super(MyWebView, self).__init__(None)
    QTimer.singleShot(0, self.startServer)

  def startServerReal(self):
    print "b"
    ioserver = SocketIOServer(('0.0.0.0', 8080), SocketApp(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843))
    print "c"
    QTimer.singleShot(0, self.loadPage)
    ioserver.serve_forever()

  def startServer(self):
    print "a"
    gevent.spawn(self.startServerReal)
    #QTimer.singleShot(50, self.loadPage)

  def loadPage(self):
    print "d"
    self.load(QUrl("http://localhost:8080/client/index.html"))

  def closeEvent(self, event):
    event.accept()

app = QApplication(sys.argv)
web = MyWebView()
web.show()
web.raise_()
#web.showFullScreen()
sys.exit(app.exec_())
