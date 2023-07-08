from multiprocessing import Process
import multiprocessing
import time
import serial
import RPi.GPIO as gpio

### ANGLE DETECT IMPORT BEGIN ###
import numpy as np
import matplotlib.pyplot as plt
import math as m
import pandas as pd
import os
import openpyxl
### ANGLE DETECT IMPORT END ###

DESCRIBE_YOURSELF_FLAG = "0".encode('utf-8')
MODE_SELECT = "2".encode('utf-8') # 1 for auto, 2 for manual.
IFFT_SELECT = "B".encode('utf-8') # A for enabled, B for disabled.
SEARCH_SEC = "8".encode('utf-8') # complement of 10.
SEARCH_SEC_INT = 2
BANDWIDTH_SELECT = "Z".encode('utf-8') # default is 3. for 5,7,9,11,13 > Y,X,W,V,U respectively.
DATAS_PER_BAND = 75
WAIT_FOR_POOL = 15
ANGLE_TRAIN_SELECTION = 1 # 1 for train mode, 2 for detection mode.
USEFUL_PRODUCT = DATAS_PER_BAND*SEARCH_SEC_INT
permissionFlag = [0,0,0,0]
lastDecision = ''
counter  = 0
# setting up the trigger.
EXTERNAL_TRIGGER_PIN = 20
gpio.setmode(gpio.BCM)
gpio.setup(EXTERNAL_TRIGGER_PIN, gpio.OUT)
gpio.setwarnings(False)

q1, q2, q3, q4 = multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() # Queues for processes.

USBports = [serial.Serial(), serial.Serial(), serial.Serial(), serial.Serial()]
UARTport = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=0)
def DetectWhichPort():
    global USBports
    for i in range(0, 4):
        try:
            port = serial.Serial("/dev/ttyACM"+str(i), baudrate=115200, timeout=0)
            port.write(DESCRIBE_YOURSELF_FLAG)
            data = port.readline()
            while data == b'':
                data = port.readline()
            queue = int(data.decode('utf-8'))
            USBports[queue-1] = port
        except:
            None

def Config(port):
    port.write(MODE_SELECT)
    time.sleep(0.1)
    port.write(IFFT_SELECT)
    time.sleep(0.1)
    port.write(SEARCH_SEC)
    time.sleep(0.1)
    port.write(BANDWIDTH_SELECT)
    time.sleep(0.1)
    return 1

def MyProc1(port):
    Config(port)
    global q1, permissionFlag
    while 1:
        if permissionFlag[0]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                q1.put(data.decode('utf-8'))
                if q1.qsize() == (USEFUL_PRODUCT):
                    permissionFlag[0] = 0
            except:
                None

def MyProc2(port):
    Config(port)
    global q2, permissionFlag
    while 1:
        if permissionFlag[1]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                q2.put(data.decode('utf-8'))
                if q2.qsize() == (USEFUL_PRODUCT):
                    permissionFlag[1] = 0
            except:
                None

def MyProc3(port):
    Config(port)
    global q3, permissionFlag
    while 1:
        if permissionFlag[2]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                q3.put(data.decode('utf-8'))
                if q3.qsize() == (USEFUL_PRODUCT):
                    permissionFlag[2] = 0
            except:
                None    

def MyProc4(port):
    Config(port)
    global q4, permissionFlag
    while 1:
        if permissionFlag[3]:
            try:
                data = port.readline()
                while data == b'':
                    data = port.readline()
                q4.put(data.decode('utf-8'))
                if q4.qsize() == (USEFUL_PRODUCT):
                    permissionFlag[3] = 0
            except:
                None
        
def Trigger():
    global permissionFlag
    while 1:
        if permissionFlag[0] == 0 and permissionFlag[1] == 0 and permissionFlag[2] == 0 and permissionFlag[3] == 0:
            permissionFlag = [1,1,1,1]
            gpio.output(EXTERNAL_TRIGGER_PIN, gpio.HIGH)
            return 1
        else:
            continue

def LastDecisionWriter():
    global LastDecision
    while 1:
        UARTport.write(LastDecision.encode('utf-8'))


if __name__ == "__main__":
    try:
        DetectWhichPort() # USBports list is modified and sorted by sensor locations. (1, 2, 3, 4)
    except:
        print("SENSORS COULD NOT BE IDENTIFIED. SCRIPT ABORTED.")
        exit()

    try:
        f1 = open("data1.txt", "a")
        f2 = open("data2.txt", "a")
        f3 = open("data3.txt", "a")
        f4 = open("data4.txt", "a")
    except:
        None
    
    p1 = Process(target=MyProc1, args=(USBports[0],))
    p2 = Process(target=MyProc2, args=(USBports[1],))
    p3 = Process(target=MyProc3, args=(USBports[2],))
    p4 = Process(target=MyProc4, args=(USBports[3],))
    p5 = Process(target=LastDecisionWriter)

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    firstSonarList = []
    secondSonarList = []
    thirdSonarList = []
    fourthSonarList = []

    Trigger() # Hidrofondan veriyi okumaya başla.

    while 1:
        waitSeconds = int(SEARCH_SEC_INT * 1.6)
        time.sleep(waitSeconds) # wait till sensors sense the environment.
        permissionFlag = [0,0,0,0] # dont listen just a bit
        for i in range(q1.qsize()):
            firstSonarList.append(float(q1.get()))
            arr1_n = np.array(firstSonarList)
        for i in range(q2.qsize()):
            secondSonarList.append(float(q2.get()))
            arr2_n = np.array(secondSonarList)
        for i in range(q3.qsize()):
            thirdSonarList.append(float(q3.get()))
            arr3_n = np.array(thirdSonarList)
        for i in range(q4.qsize()):
            fourthSonarList.append(float(q4.get()))
            arr4_n = np.array(fourthSonarList)
        

        for i in range(len(firstSonarList)):
            f1.write(str((i+1)) + str(firstSonarList[i]) + "\n")

        for i in range(len(secondSonarList)):
            f2.write(str((i+1)) + str(secondSonarList[i]) + "\n")

        for i in range(len(thirdSonarList)):
            f3.write(str((i+1)) + str(thirdSonarList[i]) + "\n")

        for i in range(len(fourthSonarList)):
            f4.write(str((i+1)) + str(fourthSonarList[i]) + "\n")

        USBports[0].reset_input_buffer()
        USBports[1].reset_input_buffer()
        USBports[2].reset_input_buffer()
        USBports[3].reset_input_buffer()

        maxIndex = [0,0,0,0]
        for i in range(len(firstSonarList)):
            if firstSonarList[i] > maxIndex[0]:
                maxIndex[0] = firstSonarList[i]

        for i in range(len(secondSonarList)):
            if secondSonarList[i] > maxIndex[1]:
                maxIndex[1] = secondSonarList[i]

        for i in range(len(thirdSonarList)):
            if thirdSonarList[i] > maxIndex[2]:
                maxIndex[2] = thirdSonarList[i]

        for i in range(len(fourthSonarList)):
            if fourthSonarList[i] > maxIndex[3]:
                maxIndex[3] = fourthSonarList[i]
        
#sağ arka 1      3
#sol arka 3      2
#aracın sağ ön 2  4
#aracın sol ön 5 1
        

        if maxIndex[0] > maxIndex[1] and maxIndex[0] > maxIndex[2] and maxIndex[0] > maxIndex[3]: #sonar birin yüksek olma durumu


        elif maxIndex[1] > maxIndex[0] and maxIndex[1] > maxIndex[2] and maxIndex[1] > maxIndex[3]: #sonar 2 nin yüksek olma durumu
            LastDecision = "-90"

        elif maxIndex[2] > maxIndex[0] and maxIndex[2] > maxIndex[1] and maxIndex[2] > maxIndex[3]: #sonar üçün yüksek olma druum
            lastDecision = -90

        elif maxIndex[3] > maxIndex[0] and maxIndex[3] > maxIndex[1] and maxIndex[3] > maxIndex[2]: #somar 4 ün yüksek olma durmu
            a = maxIndex[3] - maxIndex[1]
            b = maxIndex[3] - maxIndex[2]
            if(a>b):
                lastDecision = 10
                counter = counter +1
                if(counter == 3):
                    lastDecision = 0
            else:
                lastDecision = -10
                counter = counter - 1
                if(lastDecision == -3):
                    lastDecision = 0

        """
        choose = "-"
        while 1:
            is_g = UARTport.readline()
            if is_g.decode('utf-8') == "g":
                choose = "g"
                break
        """

        choose = "g" # it is just for debug. default is 1.
        if choose == "0":
            p1.terminate() # kill all processes
            p2.terminate()
            p3.terminate()
            p4.terminate()
            USBports[0].close() # close all ports
            USBports[1].close()
            USBports[2].close()
            USBports[3].close()
            UARTport.close()
            f1.close() # close all files
            f2.close()
            f3.close()
            f4.close()
            exit()
        elif choose == "g":
            Trigger()
            time.sleep(0.1)
            gpio.output(EXTERNAL_TRIGGER_PIN, gpio.LOW)
            choose = "-"
            continue
        else:
            None