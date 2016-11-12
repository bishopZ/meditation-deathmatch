#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()
import gevent

import numpy as np

import sys
import liblo
import datetime


class MuseOSC:

    def __init__(self, port=None):
        try:
            self.server = liblo.Server(port, liblo.TCP)
        except liblo.ServerError as err:
            sys.exit(str(err))
        self.server.add_method(None, None, self.callback)

    def blob_to_hex(self, b):
        return " ".join([(hex(v/16).upper()[-1] +
                          hex(v % 16).upper()[-1]) for v in b])

    def callback(self, path, args, types, src):
        write = sys.stdout.write
        absolutes = ['/muse/elements/low_freqs_absolute',
                     '/muse/elements/alpha_absolute',
                     '/muse/elements/beta_absolute',
                     '/muse/elements/delta_absolute',
                     '/muse/elements/gamma_absolute',
                     '/muse/elements/theta_absolute']
        relatives = ['/muse/elements/alpha_relative',
                     '/muse/elements/beta_relative',
                     '/muse/elements/delta_relative',
                     '/muse/elements/gamma_relative',
                     '/muse/elements/theta_relative']
        raw_ffts = ['/muse/elements/raw_fft0',
                    '/muse/elements/raw_fft1',
                    '/muse/elements/raw_fft2',
                    '/muse/elements/raw_fft3']
        session_scores = ['/muse/elements/alpha_session_score',
                          '/muse/elements/beta_session_score',
                          '/muse/elements/delta_session_score',
                          '/muse/elements/gamma_session_score',
                          '/muse/elements/theta_session_score']
        if (path == '/muse/elements/experimental/concentration'):
            self.attention = args[0]
            # print "CONCENTRATION " + str(args[0])
            pass
        elif (path == '/muse/elements/experimental/mellow'):
            self.meditation = args[0]
            # print "MELLOW " + str(args[0])
            pass
        elif (path == '/muse/eeg'):
            pass
        elif (path == '/muse/batt'):
            pass
        elif (path == '/muse/eeg/dropped_samples'):
            pass
        elif (path == '/muse/acc'):
            pass
        elif (path == '/muse/config'):
            pass
        elif (path == '/muse/version'):
            pass
        elif (path == '/muse/drlref'):
            pass
        elif (path == '/muse/eeg/quantization'):
            pass
        elif (path == '/muse/elements/horseshoe'):
            pass
        elif (path == '/muse/elements/is_good'):
            pass
        elif (path == '/muse/elements/blink'):
            pass
        elif (path == '/muse/elements/jaw_clench'):
            pass
        elif (path == '/muse/elements/touching_forehead'):
            pass
        elif (path in absolutes):
            pass
        elif (path in relatives):
            pass
        elif (path in session_scores):
            pass
        elif (path in raw_ffts):
            if (path == '/muse/elements/raw_fft0'):
                self.raw_fft0 = args
                C = np.abs(args)
                Fs = 220
                Band = [1, 4, 8, 10, 13, 18, 31, 41, 50]
                Power = np.zeros(len(Band)-1)
                # based on pyeeg bin_power function
                for Freq_Index in xrange(0, len(Band)-1):
                    Freq = float(Band[Freq_Index])
                    Next_Freq = float(Band[Freq_Index+1])
                    idx1 = int(np.floor(Freq/Fs*len(C)))
                    idx2 = int(np.floor(Next_Freq/Fs*len(C)))
                    Power[Freq_Index] = sum(C[idx1:idx2])
                self.waves_vector = Power.tolist()
                # bin_powers, bin_relative = pyeeg.bin_power(args, bands, 220) # problem
                # self.waves_vector = bin_powers
            elif (path == '/muse/elements/raw_fft1'):
                self.raw_fft1 = args
            elif (path == '/muse/elements/raw_fft2'):
                self.raw_fft2 = args
            elif (path == '/muse/elements/raw_fft3'):
                self.raw_fft3 = args
        else:
            write(path + " ,")
            write(types)
            for a, t in zip(args, types):
                write(" ")
                if t is None:
                    write("[unknown type]")
                elif t == 'b':
                    write("[" + self.blob_to_hex(a) + "]")
                else:
                    write(str(a))
            write('\n')

    def fmt_timestamp(self):
        obj = datetime.datetime
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        return obj.now().strftime(fmt)

    def run(self):
        while True:
            self.iterate()
            gevent.sleep(0.0001)

    def iterate(self):
        self.server.recv(1)


class GameHeadset(MuseOSC):

    attention = 0
    meditation = 0
    waves_vector = [0, 0, 0, 0, 0, 0, 0, 0]
    raw_fft0 = []
    raw_fft1 = []
    raw_fft2 = []
    raw_fft3 = []

    def __init__(self, *args, **kwargs):
        MuseOSC.__init__(self, *args, **kwargs)

    def disconnect(self):
        pass

    def get_json(self):
        waves_vector = self.waves_vector
        waves_vector = [el * 300 for el in waves_vector]
        meditation = 100 * self.meditation
        attention = 100 * self.attention
        #poor_signal = self.get('poor_signal')
        poor_signal = 0
        packet = {
            'eSense': {
                'meditation': meditation,
                'attention': attention,
            },
            'eegPower': {
                'delta': waves_vector[0],
                'theta': waves_vector[1],
                'lowAlpha': waves_vector[2],
                'highAlpha': waves_vector[3],
                'lowBeta': waves_vector[4],
                'highBeta': waves_vector[5],
                'lowGamma': waves_vector[6],
                'highGamma': waves_vector[7]
            },
            'FFT': {
                'raw0': self.raw_fft0,
                'raw1': self.raw_fft1,
                'raw2': self.raw_fft2,
                'raw3': self.raw_fft3
            },
            'poorSignalLevel': poor_signal
        }
        # print(packet)
        return packet


if __name__ == '__main__':
    #print "band,channel,value,time,whose"
    app = MuseOSC(5001)
    try:
        app.run()
    except KeyboardInterrupt:
        del app
