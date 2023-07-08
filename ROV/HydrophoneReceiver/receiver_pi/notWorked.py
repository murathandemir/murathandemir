from multiprocessing import Process
import threading
import serial
import time

def threadPort(openedPort):
    while True:
        try:
            data = openedPort.read()
            try:
                print(data)
                print("\n")
            except:
                continue
        except:
            continue


def processPort(selectedPort1, selectedPort2):
    try:
        open_selectedPort1 = serial.Serial(selectedPort1, baudrate=115200, timeout=0)
        global th1 = threading.Thread(target=threadPort, args=(open_selectedPort1,))
        th1.start()
    except:
        print("Error opening serial port\n")
    
    try:
        open_selectedPort2 = serial.Serial(selectedPort2, baudrate=115200, timeout=0)
        global th2 = threading.Thread(target=threadPort, args=(open_selectedPort2,))
        th2.start()
    except:
        print("Error opening serial port\n")


if __name__ == '__main__':
    ports = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3", "/dev/ttyACM4", "/dev/ttyACM5"]
    try:
        prc1 = Process(target=processPort, args=(ports[0], ports[1],))
        prc1.start()
    except:
        print("Error opening process for port0 and port1\n")
    
    try:
        prc2 = Process(target=processPort, args=(ports[2], ports[3],))
        prc2.start()
    except:
        print("Error opening process for port2 and port3\n")
    
    try:
        prc3 = Process(target=processPort, args=(ports[4], ports[5],))
        prc3.start()
    except:
        print("Error opening process for port4 and port5\n")
    