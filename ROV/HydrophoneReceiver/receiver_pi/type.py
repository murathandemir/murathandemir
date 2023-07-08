import serial

openedPort = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0)
print(type(openedPort))