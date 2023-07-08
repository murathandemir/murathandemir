from multiprocessing import Process
import RPi.GPIO as gpio
import threading
import serial
import time
import psutil

# Constants
MESSAGE_DETECT_WHO = "0".encode("utf-8")
MESSAGE_INVERSE_FFT_DISABLE = "A".encode("utf-8")
MESSAGE_INVERSE_FFT_ENABLE = "B".encode("utf-8")
MESSAGE_SEARCH_1SEC = "9".encode("utf-8")
MESSAGE_SEARCH_2SEC = "8".encode("utf-8")
MESSAGE_SEARCH_3SEC = "7".encode("utf-8")
MESSAGE_SEARCH_4SEC = "6".encode("utf-8")
MESSAGE_SEARCH_5SEC = "5".encode("utf-8")
INTERRUPT_GPIO_PIN1 = 20
INTERRUPT_GPIO_PIN2 = 21

try :
    UARTport = serial.Serial("/dev/ttyS0, baudrate=115200, timeout=0")
except:
    None

USBports = [serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0),
            serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=0),
            serial.Serial("/dev/ttyACM2", baudrate=115200, timeout=0),
            serial.Serial("/dev/ttyACM3", baudrate=115200, timeout=0)]

identificators = [0, 0, 0, 0]
status = [0, 0, 0]
dataPort1 = []
dataPort2 = []
dataPort3 = []
dataPort4 = []
            
def Proc1(port):
    global identificators
    global status
    global dataPort1

    port.write(MESSAGE_DETECT_WHO)
    data = port.readline()
    while data == "":
        data = port.readline()
    identificators[0] = int(data.decode("utf-8"))

    port.write(MESSAGE_INVERSE_FFT_DISABLE)
    time.sleep(0.1)
    port.write(MESSAGE_SEARCH_2SEC)
    time.sleep(0.1)
    port.write("1".encode("utf-8"))
    time.sleep(0.1)
    port.write("Z".encode("utf-8"))

    while 1:
        if status == [0, 0, 0]:
            try:
                data = port.readline()
                data = data.decode("utf-8")
                while data == b'':
                    data = port.readline()
                print("birinci : " + data.decode("utf-8"))
                dataPort1.append(data.decode("utf-8"))
                status = [1, 0, 0]
            except:
                continue

def Proc2(port):
    global identificators
    global status
    global dataPort2

    port.write(MESSAGE_DETECT_WHO)
    data = port.readline()
    while data == "":
        data = port.readline()
    identificators[1] = int(data.decode("utf-8"))

    port.write(MESSAGE_INVERSE_FFT_DISABLE)
    time.sleep(0.1)
    port.write(MESSAGE_SEARCH_2SEC)
    time.sleep(0.1)
    port.write("2".encode("utf-8"))
    time.sleep(0.1)
    port.write("Z".encode("utf-8"))

    while 1:
        if status == [1, 0, 0]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                print("ikinci : " + data.decode("utf-8"))
                dataPort2.append(data.decode("utf-8"))
                status = [1, 1, 0]
            except:
                continue

def Proc3(port):
    global identificators
    global status
    global dataPort3

    port.write(MESSAGE_DETECT_WHO)
    data = port.readline()
    while data == "":
        data = port.readline()
    identificators[2] = int(data.decode("utf-8"))

    port.write(MESSAGE_INVERSE_FFT_DISABLE)
    time.sleep(0.1)
    port.write(MESSAGE_SEARCH_2SEC)
    time.sleep(0.1)
    port.write("3".encode("utf-8"))
    time.sleep(0.1)
    port.write("Z".encode("utf-8"))

    while 1:
        if status == [1, 1, 0]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                print("ucuncu : " + data.decode("utf-8"))
                dataPort3.append(data.decode("utf-8"))
                status = [1, 1, 1]
            except:
                continue

def Proc4(port):
    global identificators
    global status
    global dataPort4

    port.write(MESSAGE_DETECT_WHO)
    data = port.readline()
    while data == "":
        data = port.readline()
    identificators[3] = int(data.decode("utf-8"))

    port.write(MESSAGE_INVERSE_FFT_DISABLE)
    time.sleep(0.1)
    port.write(MESSAGE_SEARCH_2SEC)
    time.sleep(0.1)
    port.write("4".encode("utf-8"))
    time.sleep(0.1)
    port.write("Z".encode("utf-8"))

    while 1:
        if status == [1, 1, 1]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                print("dorduncu : " + data.decode("utf-8"))
                dataPort4.append(data.decode("utf-8"))
                status = [0, 0, 0]
            except:
                continue

if __name__ == "__main__":
    P1 = Process(target=Proc1, args=(USBports[0],))
    P2 = Process(target=Proc2, args=(USBports[1],))
    P3 = Process(target=Proc3, args=(USBports[2],))
    P4 = Process(target=Proc4, args=(USBports[3],))

    P1.start()
    print("P1 started")
    P2.start()
    print("P2 started")
    P3.start()
    print("P3 started")
    P4.start()
    print("P4 started")