import serial
import time

port = serial.Serial("/dev/ttyACM3", baudrate=115200, timeout=0)

while(1):
	x = input()
	port.write(x.encode())
	while(1):
		y = port.readline()
		if(y.decode("utf-8") == ""):
			continue
		else:
			print(y)
			break
