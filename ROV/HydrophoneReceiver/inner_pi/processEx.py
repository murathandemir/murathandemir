from multiprocessing import Process
import time
import serial

port1 = serial.Serial("/dev/ttyACM0", 115200, timeout=0)
port2 = serial.Serial("/dev/ttyACM1", 115200, timeout=0)
port3 = serial.Serial("/dev/ttyACM2", 115200, timeout=0)
port4 = serial.Serial("/dev/ttyACM3", 115200, timeout=0)

def P1():
    while 1:
        data = port1.readline()
        if data != b'':
            print(data)
            continue
        else:
            continue

def P2():
    while 1:
        data = port2.readline()
        if data != b'':
            print(data)
            continue
        else:
            continue

def P3():
    while 1:
        data = port3.readline()
        if data != b'':
            print(data)
            continue
        else:
            continue

def P4():
    while 1:
        data = port4.readline()
        if data != b'':
            print(data)
            continue
        else:
            continue

if __name__ == "__main__":
    p1 = Process(target=P1)
    p2 = Process(target=P2)
    p3 = Process(target=P3)
    p4 = Process(target=P4)
    print("1i actim")
    p1.start()
    print("2yi actim")
    p2.start()
    print("3u actim")
    p3.start()
    print("4u actim")
    p4.start()
