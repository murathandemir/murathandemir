from multiprocessing import Process
import threading
import serial
import time

dataSensor1, dataSensor2, dataSensor3, dataSensor4, dataSensor5, dataSensor6 = b'', b'', b'', b'', b'', b''
openedPort1, openedPort2, openedPort3, openedPort4, openedPort5, openedPort6 = None, None, None, None, None, None
def threadSensor1(sensor1):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort1 = serial.Serial(sensor1, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor1 Error: No connection\n")
                break
        
        try:
            global dataSensor1
            dataSensor1 = openPort1.readline()
        except:
            if(not openedPort1):
                print("Sensor1 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor1.decode("utf-8") is not ""):
                print("Sensor1 Data: " + dataSensor1.decode("utf-8") + "\n")
        except:
            print("Sensor1 Error: Unable to read data\n")
            continue

def threadSensor2(sensor2):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort2 = serial.Serial(sensor2, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor2 Error: No connection\n")
                break
        
        try:
            global dataSensor2
            dataSensor2 = openPort2.readline()
        except:
            if(not openedPort2):
                print("Sensor2 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor2.decode("utf-8") is not ""):
                print("Sensor2 Data: " + dataSensor2.decode("utf-8") + "\n")
        except:
            print("Sensor2 Error: Unable to read data\n")
            continue
    
def threadSensor3(sensor3):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort3 = serial.Serial(sensor3, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor3 Error: No connection\n")
                break
        
        try:
            global dataSensor3
            dataSensor3 = openPort3.readline()
        except:
            if(not openedPort3):
                print("Sensor3 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor3.decode("utf-8") is not ""):
                print("Sensor3 Data: " + dataSensor3.decode("utf-8") + "\n")
        except:
            print("Sensor3 Error: Unable to read data\n")
            continue

def threadSensor4(sensor4):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort4 = serial.Serial(sensor4, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor4 Error: No connection\n")
                break
        
        try:
            global dataSensor4
            dataSensor4 = openPort4.readline()
        except:
            if(not openedPort4):
                print("Sensor4 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor4.decode("utf-8") is not ""):
                print("Sensor4 Data: " + dataSensor4.decode("utf-8") + "\n")
        except:
            print("Sensor1 Error: Unable to read data\n")
            continue
def threadSensor5(sensor5):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort5 = serial.Serial(sensor5, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor5 Error: No connection\n")
                break
        
        try:
            global dataSensor5
            dataSensor5 = openPort5.readline()
        except:
            if(not openedPort5):
                print("Sensor5 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor5.decode("utf-8") is not ""):
                print("Sensor5 Data: " + dataSensor5.decode("utf-8") + "\n")
        except:
            print("Sensor5 Error: Unable to read data\n")
            continue

def threadSensor6(sensor6):
    openedFlag = 0
    while(1):
        if(not openedFlag):
            try:
                openPort6 = serial.Serial(sensor6, baudrate=115200, timeout=0)
                openedFlag = 1
            except:
                print("Sensor6 Error: No connection\n")
                break
        
        try:
            global dataSensor6
            dataSensor6 = openPort6.readline()
        except:
            if(not openedPort6):
                print("Sensor6 Error: Connection Lost.\n")
                break
            else:
                continue

        try:
            if(dataSensor6.decode("utf-8") is not ""):
                print("Sensor6 Data: " + dataSensor6.decode("utf-8") + "\n")
        except:
            print("Sensor6 Error: Unable to read data\n")
            continue
    
def processSensor12(sensor1, sensor2):
    th1 = threading.Thread(target=threadSensor1, args=(sensor1, ))
    th2 = threading.Thread(target=threadSensor2, args=(sensor2, ))
    th1.start()
    th2.start()

    th1.join()
    th2.join()
    while(th1.is_alive() or th2.is_alive()):
        continue

def processSensor34(sensor3, sensor4):
    th3 = threading.Thread(target=threadSensor3, args=(sensor3, ))
    th4 = threading.Thread(target=threadSensor4, args=(sensor4, ))
    th3.start()
    th4.start()

    th3.join()
    th4.join()
    while(th3.is_alive() or th4.is_alive()):
        continue

def processSensor56(sensor5, sensor6):
    th5 = threading.Thread(target=threadSensor5, args=(sensor5, ))
    th6 = threading.Thread(target=threadSensor6, args=(sensor6, ))
    th5.start()
    th6.start()

    th5.join()
    th6.join()
    while(th5.is_alive() or th6.is_alive()):
        continue

if __name__ == "__main__":
    prc12 = Process(target=processSensor12, args=("/dev/ttyACM0", "/dev/ttyACM1",))
    prc34 = Process(target=processSensor34, args=("/dev/ttyACM2", "/dev/ttyACM3",))
    prc56 = Process(target=processSensor56, args=("/dev/ttyACM4", "/dev/ttyACM5",))
    prc12.start()
    prc34.start()
    prc56.start()
#
#   prc12.join()
#   prc34.join()
#   prc56.join()
#   


