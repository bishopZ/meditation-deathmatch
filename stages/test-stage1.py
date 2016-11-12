#!/usr/bin/env python

import serial
import gevent

# in Windows, First param is the Com Port -1, so COM6 = 5
# in Linux, First param is /dev/ttyACM0
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
gevent.sleep(1)


ser.write("1,a\n") # red
gevent.sleep(0.4)

ser.write("1,b\n") # yellow
gevent.sleep(0.4)

ser.write("1,c\n") # green
gevent.sleep(0.4)
#ser.write("1,d\n") # blue
