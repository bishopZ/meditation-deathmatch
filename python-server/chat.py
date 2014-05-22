from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

##########################################################
import gevent
import platform
import sys, time
from pymindwave import headset
from pymindwave.pyeeg import bin_power


def raw_to_spectrum(rawdata):
    flen = 50
    spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
    return spectrum

##########################################################


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    hs = {}
    connected = False

    def my_loop(self):
        while True:
            if (self.connected):
                print "fire!"
                #print 'attention {0}, meditation {1}'.format(self.hs.get('attention'), self.hs.get('meditation'))
                #print 'alpha_waves {0}'.format(self.hs.get('alpha_waves'))
                #print 'blink_strength {0}'.format(self.hs.get('blink_strength'))
                #print 'raw data:'
                #print self.hs.get('rawdata')
                t = time.time()
                waves_vector = self.hs.get('waves_vector')
                meditation = self.hs.get('meditation')
                attention = self.hs.get('attention')
                spectrum = raw_to_spectrum(self.hs.get('rawdata')).tolist()
            
                packet = {
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
                  }
                }
                
                packets = [packet, packet]
                self.emit('mindEvent', packets)
            gevent.sleep(1)
    
    def connect_hs(self):
        print "a"
        if platform.system() == 'Darwin':
            self.hs = headset.Headset('/dev/tty.MindWaveMobile-DevA')
            print "b"
        else:
            self.hs = headset.Headset('/dev/ttyUSB0')
        print "c"
        gevent.sleep(1)
        print "d"
        if self.hs.get_state() != 'connected':
            self.hs.disconnect()
            print "e"
        print "f"
        while self.hs.get_state() != 'connected':
            print "g"
            gevent.sleep(1)
            print "h"
            print 'current state: {0}'.format(self.hs.get_state())
            if (self.hs.get_state() == 'standby'):
                print 'trying to connect...'
                self.hs.connect()
        self.connected = True 
        print 'now connected!'

    def on_request_connect(self):
        print "will connect"
        gevent.Greenlet.spawn(self.connect_hs)
        gevent.Greenlet.spawn(self.my_loop)

#    def on_nickname(self, nickname):
#        self.request['nicknames'].append(nickname)
#        self.socket.session['nickname'] = nickname
#        self.broadcast_event('announcement', '%s has connected' % nickname)
#        self.broadcast_event('nicknames', self.request['nicknames'])
#        ######################################################################
#        print "will connect"
#        gevent.Greenlet.spawn(self.connect_hs)
#        gevent.Greenlet.spawn(self.my_loop)
#        ######################################################################
#        # Just have them join a default-named room
#        self.join('main_room')

    def recv_disconnect(self):
        # Remove nickname from the list.
        nickname = self.socket.session['nickname']
        self.request['nicknames'].remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.request['nicknames'])

        self.disconnect(silent=True)

    def on_user_message(self, msg):
        self.emit_to_room('main_room', 'msg_to_room',
            self.socket.session['nickname'], msg)

    def recv_message(self, message):
        print "PING!!!", message

class Application(object):
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
                return not_found(start_response)

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
            socketio_manage(environ, {'': ChatNamespace}, self.request)
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']

if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()