import time
import serial


// in Windows, First param is the Com Port -1, so COM6 = 5
// in Linux, First param is /dev/usb2
ser = serial.Serial(5, 9600, timeout=2)
 
ser.write("1,a\n")
time.sleep(1)
ser.write("1,b\n")
time.sleep(1)
ser.write("1,c\n")
time.sleep(1)
ser.write("1,d\n")
time.sleep(1)
ser.write("1,e\n")
time.sleep(1)
ser.write("1,f\n")
time.sleep(1)
ser.write("1,000,000,000\n")
time.sleep(1)
ser.write("1,255,255,255\n")
time.sleep(1)
ser.write("1,000,000,000\n")

ser.write("2,a\n")
time.sleep(1)
ser.write("2,b\n")
time.sleep(1)
ser.write("2,c\n")
time.sleep(1)
ser.write("2,d\n")
time.sleep(1)
ser.write("2,e\n")
time.sleep(1)
ser.write("2,f\n")
time.sleep(1)
ser.write("2,000,000,000\n")
time.sleep(1)
ser.write("2,255,255,255\n")
time.sleep(1)
ser.write("2,000,000,000\n")