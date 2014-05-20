import re
import time
import json
import unicodedata

import gevent
from gevent import monkey

from pymindwave import headset
from pymindwave.pyeeg import bin_power

monkey.patch_all()

# connect to the headset
hs = None
hs = headset.Headset('/dev/tty.MindWaveMobile-DevA-1')
hs.disconnect()
time.sleep(1)
print 'connecting to headset...'
hs.connect()
time.sleep(1)
while hs.get('state') != 'connected':
    print hs.get('state')
    time.sleep(0.5)
    if hs.get('state') == 'standby':
        hs.connect()
        print 'retrying connecting to headset'

def raw_to_spectrum(rawdata):
    flen = 50
    spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
    return spectrum

while True:
    t = time.time()
    waves_vector = hs.get('waves_vector')
    meditation = hs.get('meditation')
    attention = hs.get('attention')
    spectrum = raw_to_spectrum(hs.get('rawdata')).tolist()

    s = {'timestamp': t,
         'eSense': {
           'meditation': meditation,
           'attention': attention,
         },
         'eegPower' : {
           'raw_spectrum': spectrum,
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
    s = json.dumps(s)
    print s
    gevent.sleep(0.4)
