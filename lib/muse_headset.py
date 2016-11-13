#!/usr/bin/env python

import gevent
import numpy as np
import sys
import liblo
from gevent import monkey
monkey.patch_all()


class MuseOSC:

    def __init__(self, port=None, return_packet_cb=None):
        self.return_packet_cb = return_packet_cb
        try:
            self.server = liblo.Server(port, liblo.TCP)
        except liblo.ServerError as err:
            sys.exit(str(err))
        self.server.add_method(None, None, self.callback)

    def callback(self, path, args, types, src):
        raw_ffts = ['/muse/elements/raw_fft0',
                    '/muse/elements/raw_fft1',
                    '/muse/elements/raw_fft2',
                    '/muse/elements/raw_fft3']
        if (path == '/muse/elements/experimental/mellow'):
            self.meditation = args[0]
        elif (path in raw_ffts):
            args = list(np.abs(args) * 20)
            if (path == '/muse/elements/raw_fft0'):
                self.raw_fft0 = args
                C = np.abs(args)
                Fs = 220
                Band = [1, 4, 8, 10, 13, 18, 31, 41, 50]
                Power = np.zeros(len(Band)-1)
                # based on pyeeg bin_power function
                for Freq_Index in range(0, len(Band)-1):
                    Freq = float(Band[Freq_Index])
                    Next_Freq = float(Band[Freq_Index+1])
                    idx1 = int(np.floor(Freq/Fs*len(C)))
                    idx2 = int(np.floor(Next_Freq/Fs*len(C)))
                    Power[Freq_Index] = sum(C[idx1:idx2])
                self.waves_vector = Power.tolist()
            elif (path == '/muse/elements/raw_fft1'):
                self.raw_fft1 = args
            elif (path == '/muse/elements/raw_fft2'):
                self.raw_fft2 = args
            elif (path == '/muse/elements/raw_fft3'):
                self.raw_fft3 = args
        if (self.return_packet_cb):
            self.return_packet_cb(path, args)

    def run(self):
        while True:
            self.iterate()
            gevent.sleep(0.0001)

    def iterate(self):
        self.server.recv(1)


if __name__ == '__main__':
    app = MuseOSC(5001)
    try:
        app.run()
    except KeyboardInterrupt:
        del app
