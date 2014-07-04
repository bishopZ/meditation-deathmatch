#!/usr/bin/env python

from socketio.server import SocketIOServer
from mdma.socketiogame import SocketApp

def socketio_server():
    server = SocketIOServer(('0.0.0.0', 0), SocketApp(), policy_server=False)
    server.start()
    port = server.socket.getsockname()[1]
    print 'Listening on port '+str(port)
    server.serve_forever()

if __name__ == '__main__':
  socketio_server()
