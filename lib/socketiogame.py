#!/usr/bin/env python

import os
import serial
import gevent

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from muse_headset import MuseOSC
from gevent import monkey
from time import time

monkey.patch_all()


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
    hs1_greenlet = None
    hs2_greenlet = None
    useLights = True
    ser = ''
    ser_device = '/dev/ttyUSB0'
    ser_connected = False
    last_light1_update = 0
    last_light2_update = 0

    def handle_lights(self, which, meditation):
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

    def connect_hs1(self):
        self.connect_hs()

    def connect_hs2(self):
        self.connect_hs(True)

    def init_lights(self):
        if (self.useLights):
            try:
                self.ser = serial.Serial(self.ser_device, 9600, timeout=2)
                gevent.sleep(1)  # The arduino hates us if we don't wait
                self.ser_connected = True
            except:
                pass

    def handle_packet(self, headset, path, args):
        if (path == '/muse/elements/experimental/mellow'):
            curtime = time()
            light_delay = 0.2
            if (headset == 1):
                if (curtime - self.last_light1_update > light_delay):
                    # print("update lights 1")
                    self.handle_lights(1, args[0] * 100)
                    self.last_light1_update = curtime
            if (headset == 2):
                if (curtime - self.last_light2_update > light_delay):
                    # print("update lights 2")
                    self.handle_lights(2, args[0] * 100)
                    self.last_light2_update = curtime
        packet = {
            'headset': headset,
            'path': path,
            'args': args
        }
        self.emit('packet', packet)

    def handle_packet_one(self, path, args):
        self.handle_packet(1, path, args)

    def handle_packet_two(self, path, args):
        self.handle_packet(2, path, args)

    def on_request_init_lights(self):
        print("request init lights")
        self.init_lights_greenlet = gevent.Greenlet.spawn(self.init_lights)

    def on_request_connect_one(self):
        print("request connect one")
        self.hs1 = MuseOSC(5001, self.handle_packet_one)
        self.hs1_greenlet = gevent.Greenlet.spawn(self.hs1.run)

    def on_request_connect_two(self):
        print("request connect two")
        self.hs2 = MuseOSC(5002, self.handle_packet_two)
        self.hs2_greenlet = gevent.Greenlet.spawn(self.hs2.run)

    def on_request_disconnect(self):
        print("will disconnect")
        pass
