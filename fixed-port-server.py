#!/usr/bin/env python

from socketio.server import SocketIOServer
from lib.socketiogame import SocketApp


def socketio_server():
    server = SocketIOServer(('0.0.0.0', 3101), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    print 'http://localhost:'+str(port)+'/'
    server.serve_forever()

if __name__ == '__main__':
    socketio_server()
