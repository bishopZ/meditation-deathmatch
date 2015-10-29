#!/usr/bin/env python

import serial
import gevent

# in Windows, First param is the Com Port -1, so COM6 = 5
# in Linux, First param is /dev/ttyACM0
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
gevent.sleep(1)

#gevent.sleep(0.4)
#ser.write("1,c\n")
#gevent.sleep(0.4)
#ser.write("1,d\n")
#gevent.sleep(0.4)
#ser.write("1,e\n")
#gevent.sleep(0.4)
#ser.write("1,f\n")
#gevent.sleep(0.4)
#ser.write("1,000,000,000\n")
#gevent.sleep(0.4)
#ser.write("1,255,255,255\n")
#gevent.sleep(0.4)
#ser.write("1,000,000,000\n")
#
ser.write("2,a\n")
gevent.sleep(0.4)
ser.write("2,b\n")
gevent.sleep(0.4)
ser.write("2,c\n")
gevent.sleep(0.4)
#ser.write("2,d\n")
#gevent.sleep(0.4)
#ser.write("2,e\n")
#gevent.sleep(0.4)
#ser.write("2,f\n")
#gevent.sleep(0.4)
#ser.write("2,000,000,000\n")
#gevent.sleep(0.4)
#ser.write("2,255,255,255\n")
#gevent.sleep(0.4)
#ser.write("2,000,000,000\n")
