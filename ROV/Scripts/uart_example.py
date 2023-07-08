import serial
from time import sleep

port = serial.Serial("/dev/ttyS0", 115200)
port.write("1")
sleep(1)
port.write("2")
sleep(1)
port.write("3")
sleep(1)
port.write("slm ben pi")
