import os

from gevent import monkey; monkey.patch_all()
import gevent

from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from pymindwave import headset
from pymindwave.pyeeg import bin_power

class GameHeadset(headset.Headset):
  def __init__(self, *args, **kwargs):
    super(GameHeadset, self).__init__(self, *args, **kwargs)

  def raw_to_spectrum(self, rawdata):
        flen = 50
        spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
        return spectrum

  def get_json(self):
    waves_vector = self.get('waves_vector')
    meditation = self.get('meditation')
    attention = self.get('attention')
    poor_signal = self.get('poor_signal')
    spectrum = self.raw_to_spectrum(self.get('rawdata')).tolist()
    packet = {
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
    return packet

class SocketApp(object):
    def __init__(self):
        self.buffer = []
        self.request = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
          start_response('301 Redirect', [('Location', '/client/index.html'),])
          return []

        if path.startswith('client/'):
          mode = 'rb'
          if path.endswith(".png"):
            content_type = "image/png"
          elif path.endswith(".js"):
            mode = 'r'
            content_type = "text/javascript"
          elif path.endswith(".css"):
            mode = 'r'
            content_type = "text/css"
          elif path.endswith(".swf"):
            content_type = "application/x-shockwave-flash"
          else:
            mode = 'r'
            content_type = "text/html"

          try:
              data = open(path.replace('/', os.sep), mode).read()
          except Exception:
              return self.not_found(start_response)

          start_response('200 OK', [('Content-Type', content_type)])
          return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'': GameNamespace}, self.request)
        else:
            return self.not_found(start_response)

    def not_found(self, start_response):
        start_response('404 Not Found', [])
        return ['<h1>Not Found</h1>']


class GameNamespace(BaseNamespace):

    hs1 = {}
    hs2 = {}
    connected = False
    loop_greenlet = ''

    def my_loop(self):
        while True:
            if (self.connected):
                packet1 = self.hs1.get_json()
                packet2 = self.hs2.get_json()
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
        self.hs1 = GameHeadset('/dev/tty.MindWaveMobile-DevA-1')
        self.hs2 = GameHeadset('/dev/tty.MindWaveMobile-DevA')
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
