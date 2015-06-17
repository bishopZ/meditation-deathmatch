import os
import serial

from gevent import monkey
monkey.patch_all()
import gevent

from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from muse_headset import GameHeadset

from time import sleep


class SocketApp(object):
    def __init__(self):
        self.buffer = []
        self.request = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
            headers = [('Location', '/client/index.html'), ]
            start_response('301 Redirect', headers)
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
    twoPlayer = False
    useLights = True
    loop_greenlet = ''
    ser = ''
    ser_device = '/dev/ttyUSB0'
    ser_connected = False

    def handle_lights(self, which, packet):
        meditation = packet['eSense']['meditation']
        if (meditation > 90):
            color = 'c'
        elif (meditation > 80):
            color = 'b'
        elif (meditation > 75):
            color = 'e'
        else:
            color = 'a'
        if (self.ser_connected):
            self.ser.write(str(which)+","+color+"\n")

    def my_loop(self):
        while True:
            if (self.connected):
                packet1 = self.hs1.get_json()
                if (self.twoPlayer):
                    packet2 = self.hs2.get_json()
                else:
                    packet2 = packet1
                packets = [packet1, packet2]
                self.handle_lights(1, packet1)
                self.handle_lights(2, packet2)
                self.emit('mindEvent', packets)
            gevent.sleep(1)

    def disconnect_hs(self):
        if (self.connected):
            self.connected = False
            self.hs1.disconnect()
            if (self.twoPlayer):
                self.hs2.disconnect()

    def connect_hs1(self):
        self.connect_hs()

    def connect_hs2(self):
        self.connect_hs(True)

    def init_lights(self):
        if (self.useLights):
            try:
                self.ser = serial.Serial(self.ser_device, 9600, timeout=2)
                gevent.sleep(1) # The arduino hates us if we don't wait
                self.ser_connected = True
            except:
                pass

    def connect_hs(self, twoPlayer=False):
        self.hs_greenlet = gevent.Greenlet.spawn(self.init_lights)
        self.hs1 = GameHeadset(5001)
        self.hs_greenlet = gevent.Greenlet.spawn(self.hs1.run)
        if (twoPlayer):
            self.twoPlayer = True
            self.hs2 = GameHeadset(5002)
            self.hs_greenlet = gevent.Greenlet.spawn(self.hs2.run)
        self.connected = True
        pass

    def on_request_connect_one(self):
        print "will connect"
        gevent.Greenlet.spawn(self.connect_hs1)
        self.loop_greenlet = gevent.Greenlet.spawn(self.my_loop)

    def on_request_connect_two(self):
        print "will connect"
        gevent.Greenlet.spawn(self.connect_hs2)
        self.loop_greenlet = gevent.Greenlet.spawn(self.my_loop)

    def on_request_disconnect(self):
        print "will disconnect"
        if ('kill' in dir(self.loop_greenlet)):
            print "kill greenlet"
            self.loop_greenlet.kill()
        self.disconnect_hs()
