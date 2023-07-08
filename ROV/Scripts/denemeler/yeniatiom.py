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
INTERRUPT_GPIO_PIN = 20
status = [0, 0, 0, 0]

# Global variables
USBports = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
JetsonPort = "/dev/ttyS0"
openedUSBs = [serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0),
              serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=0),
              serial.Serial("/dev/ttyACM2", baudrate=115200, timeout=0),
              serial.Serial("/dev/ttyACM3", baudrate=115200, timeout=0)] # front, left, back, right
openedJetson = None

def OpenJetson(): # Write data to serial port
    global JetsonPort
    global openedJetson
    try:
        openedJetson = serial.Serial(JetsonPort, 115200, timeout=0)
        print("Jetson UART Com. Port opened successfully\n")
        return 1
    except:
        print("Error while opening Jetson UART Com. Port\n")
        return 0

def WriteJetson(data): # Write data to serial port | TAKES : string data
    global openedJetson
    if openedJetson != None:
        try:
            openedJetson.write(data)
            print("Data written successfully\n")
            return 1
        except:
            print("Error while writing Jetson UART Com. Port\n")
            return 0

def OpenUSB(portname): # Open serial port | TAKES : string portname
    try:
        port = serial.Serial(portname, 115200, timeout=0)
        print("Port opened successfully\n")
        return port
    except:
        print("Error while opening port\n")
        return 0

def ListenUSB(port): # Listen to serial port and return data | TAKES : serial.Serial Port object
    while 1:
        try:
            data = port.readline()
            data = data.decode("utf-8")
            if data != b'':
                print(data)
                return data
            continue
        except:
            print("Error while reading port\n")
            continue

def WriteUSB(port, data): # Write data to serial port | TAKES : serial.Serial Port object, string data
    try:
        port.write(data)
        print("Data written successfully\n")
        return 1
    except:
        print("Error while writing port\n")
        return 0

def InitGPIO():
    gpio.setmode(gpio.BCM)
    gpio.setup(INTERRUPT_GPIO_PIN, gpio.OUT)

def InitPorts(): # Initialize all ports and GPIO
    global USBports
    OpenJetson()

    InitGPIO()

    port = OpenUSB(USBports[0])
    DetectWho(port)
    port = OpenUSB(USBports[1])
    DetectWho(port)
    port = OpenUSB(USBports[2])
    DetectWho(port)
    port = OpenUSB(USBports[3])
    DetectWho(port)

    PortConfigure(openedUSBs[0])
    PortConfigure(openedUSBs[1])
    PortConfigure(openedUSBs[2])
    PortConfigure(openedUSBs[3])

def DetectWho(port):
    port.write(MESSAGE_DETECT_WHO)
    while 1:
        try:
            data = port.readline()
            if data != b'':
                #data = data.decode("utf-8")
                openedUSBs[int(data)-1] = port
                break
            continue
        except:
            continue
    
def PortConfigure(port): # Configure port for listening
    WriteUSB(port, MESSAGE_INVERSE_FFT_DISABLE)
    time.sleep(0.2)
    WriteUSB(port, MESSAGE_SEARCH_2SEC)
    time.sleep(0.2)
    WriteUSB(port, "1".encode("utf-8"))
    time.sleep(0.2)
    WriteUSB(port, "Z".encode("utf-8"))

        
def Proc1(port):
    global status
    dataList = []
    gpio.output(INTERRUPT_GPIO_PIN, gpio.HIGH)
    while 1:
        if status == [0, 0, 0, 0]:
            try:
                data = port.readline()
                print("bir")
                if data != b'':
                    print("proc1 > " + data)
                    status = [1, 0, 0, 0]
                    dataList.append(data)
                    continue
                continue
            except:
                continue

def Proc2(port):
    global status
    dataList = []
    gpio.output(INTERRUPT_GPIO_PIN, gpio.HIGH)
    while 1:
        if status == [1, 0, 0, 0]:
            try:
                print("iki")
                data = port.readline()
                if data != b'':
                    print("proc2 > " + data)
                    status = [1, 1, 0, 0]
                    dataList.append(data)
                    continue
                continue
            except:
                continue

def Proc3(port):
    global status
    dataList = []
    gpio.output(INTERRUPT_GPIO_PIN, gpio.HIGH)
    while 1:
        if status == [1, 1, 0, 0]:
            try:
                print("uc")
                data = port.readline()
                if data != b'':
                    print("proc3 > " + data)
                    status = [1, 1, 1, 0]
                    dataList.append(data)
                    continue
                continue
            except:
                continue

def Proc4(port):
    global status
    dataList = []
    gpio.output(INTERRUPT_GPIO_PIN, gpio.HIGH)
    while 1:
        if status == [1, 1, 1, 0]:
            try:
                data = port.readline()
                print("dort") 
                if data != b'':
                    print("proc4 > " + data.decode("utf-8"))
                    status = [0, 0, 0, 0]
                    dataList.append(data)
                    continue
                continue
            except:
                continue

if __name__ == "__main__":
    InitPorts() # ports are opened & detected which one is which.

    Process1 = Process(target=Proc1, args=(openedUSBs[0],))
    Process2 = Process(target=Proc2, args=(openedUSBs[1],))
    Process3 = Process(target=Proc3, args=(openedUSBs[2],))
    Process4 = Process(target=Proc4, args=(openedUSBs[3],))

    Process1.start()
    print("birinciyi actim\n")
    Process2.start()
    print("ikinciyi actim\n")
    Process3.start()
    print("ucuncuyu actim\n")
    Process4.start()
    print("dorduncuyu actim\n")
