#!/usr/bin/env python
# -*- coding:utf-8 -*-

import platform
import sys, time
from pymindwave import headset
from pymindwave.pyeeg import bin_power

def raw_to_spectrum(rawdata):
    flen = 50
    spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
    #print spectrum
    #print relative_spectrum
    return spectrum


if __name__ == "__main__":
    if platform.system() == 'Darwin':
        hs1 = headset.Headset('/dev/tty.MindWaveMobile-DevA-1')
        hs2 = headset.Headset('/dev/tty.MindWaveMobile-DevA')
    else:
        hs1 = headset.Headset('/dev/ttyUSB0')
        hs2 = headset.Headset('/dev/ttyUSB1')

    # wait some time for parser to udpate state so we might be able
    # to reuse last opened connection.
    time.sleep(1)
    if hs1.get_state() != 'connected':
        hs1.disconnect()

    while hs1.get_state() != 'connected':
        time.sleep(1)
        print 'current state: {0}'.format(hs1.get_state())
        if (hs1.get_state() == 'standby'):
            print 'trying to connect hs1...'
            hs1.connect()

    if hs2.get_state() != 'connected':
        hs2.disconnect()

    while hs2.get_state() != 'connected':
        time.sleep(1)
        print 'current state: {0}'.format(hs2.get_state())
        if (hs2.get_state() == 'standby'):
            print 'trying to connect hs2...'
            hs2.connect()

    print 'now connected!'
    while True:
        print 'wait 1s to collect data...'
        time.sleep(1)
        print 'hs1 attention {0}, meditation {1}'.format(hs1.get('attention'), hs1.get('meditation'))
        print 'hs1 alpha_waves {0}'.format(hs1.get('alpha_waves'))
        print 'hs1 blink_strength {0}'.format(hs1.get('blink_strength'))

        print 'hs2 attention {0}, meditation {1}'.format(hs2.get('attention'), hs2.get('meditation'))
        print 'hs2 alpha_waves {0}'.format(hs2.get('alpha_waves'))
        print 'hs2 blink_strength {0}'.format(hs2.get('blink_strength'))

        #print 'raw data:'
        #print hs.get('rawdata')
        #print raw_to_spectrum(hs.get('rawdata'))

    print 'disconnecting...'
    hs1.disconnect()
    hs1.destroy()
    hs2.disconnect()
    hs2.destroy()
    sys.exit(0)
