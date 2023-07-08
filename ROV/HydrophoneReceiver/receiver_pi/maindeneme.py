from multiprocessing import Process
import threading
import serial
import time
import queue

def threadSensor1(sensor1, q):
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
    None
def threadSensor4(sensor4):
    None
def threadSensor5(sensor5):
    None
def threadSensor6(sensor6):
    None
    
def processSensor12(sensor1, sensor2):
    queue1 = queue.Queue(maxsize=2)
    th1 = threading.Thread(target=threadSensor1, args=(sensor1, queue1, ))
    th2 = threading.Thread(target=threadSensor2, args=(sensor2, queue1, ))
    th1.start()
    th2.start()

    th1.join()
    th2.join()
    while(th1.is_alive() or th2.is_alive()):
        continue

def processSensor34(sensor3, sensor4):
    queue2 = queue.Queue(maxsize=2)
    th3 = threading.Thread(target=threadSensor3, args=(sensor3, queue2, ))
    th4 = threading.Thread(target=threadSensor4, args=(sensor4, queue2, ))
    th3.start()
    th4.start()

    th3.join()
    th4.join()
    while(th3.is_alive() or th4.is_alive()):
        continue

def processSensor56(sensor5, sensor6):
    queue3 = queue.Queue(maxsize=2)
    th5 = threading.Thread(target=threadSensor5, args=(sensor5, queue3, ))
    th6 = threading.Thread(target=threadSensor6, args=(sensor6, queue3, ))
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

    while(prc12.is_alive() or prc34.is_alive() or prc56.is_alive()):
        continue

