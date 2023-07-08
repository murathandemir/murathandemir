from multiprocessing import Process
import threading
import serial
import time

mainPermission = 1
# those are variables must be declared as global. It is necessary to data exchange between threads.
dataSensor1, dataSensor2, dataSensor3, dataSensor4, dataSensor5, dataSensor6 = b'', b'', b'', b'', b'', b''
datas = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 1
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 2
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 3  
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 4
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 5
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 7 data fetched from sensor 6
] # now datas[1][4] means 5th data fetched from sensor 2

# index 1: is the port 1 opened?
# index 2: is the port 2 opened?
# index 3: has the job of the first thread done?
# index 4: has the job of the second thread done?
# index 5: main loop controlled?
controlThread12 = [0, 0, 0, 0]
controlThread34 = [0, 0, 0, 0]
controlThread56 = [0, 0, 0, 0]

# 00 > 1. thread çalışır > 10 olur
# 10 > 2. thread çalışır > 11 olur
# 11 ise 00 olur.

def threadSensor1(serial1):
    global mainPermission
    global controlThread12
    global dataSensor1
    global datas
    if(controlThread12[1] == 0): # if the second port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor1 = serial1.readline()
                except:
                    print("Sensor1 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor1 is not b''):
                        print("Sensor1 Data: " + dataSensor1.decode("utf-8") + "\n")
                        package = dataSensor1.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[0][i] = float(temp[i])
                except:
                    print("Sensor1 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread12[2] == 0 and controlThread12[3] == 0 and mainPermission):
                try:
                    dataSensor1 = serial1.readline()
                except:
                    print("Sensor1 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor1 is not b''):
                        print("Sensor1 Data: " + dataSensor1.decode("utf-8") + "\n")
                        controlThread12[2] = 1
                        package = dataSensor1.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[0][i] = float(temp[i])
                except:
                    print("Sensor1 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor2(serial2):
    global mainPermission
    global controlThread12
    global dataSensor2
    global datas
    if(controlThread12[0] == 0): # if the first port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor2 = serial2.readline()
                except:
                    print("Sensor2 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor2 is not b''):
                        print("Sensor2 Data: " + dataSensor2.decode("utf-8") + "\n")
                        package = dataSensor2.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[1][i] = float(temp[i])
                except:
                    print("Sensor2 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread12[2] == 1 and controlThread12[3] == 0 and mainPermission):
                try:
                    dataSensor2 = serial2.readline()
                except:
                    print("Sensor2 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor2 is not b''):
                        print("Sensor2 Data: " + dataSensor2.decode("utf-8") + "\n")
                        controlThread12[3] = 1
                        package = dataSensor2.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[1][i] = float(temp[i])
                    if(controlThread12[2] == 1 and controlThread12[3] == 1):
                        controlThread12[2] = 0
                        controlThread12[3] = 0
                except:
                    print("Sensor2 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor3(serial3):
    global mainPermission
    global controlThread34
    global dataSensor3
    global datas
    if(controlThread34[1] == 0): # if the second port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor3 = serial3.readline()
                except:
                    print("Sensor3 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor3 is not b''):
                        print("Sensor3 Data: " + dataSensor3.decode("utf-8") + "\n")
                        package = dataSensor3.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[2][i] = float(temp[i])
                except:
                    print("Sensor3 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread34[2] == 0 and controlThread34[3] == 0 and mainPermission):
                try:
                    dataSensor3 = serial3.readline()
                except:
                    print("Sensor3 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor3 is not b''):
                        print("Sensor3 Data: " + dataSensor3.decode("utf-8") + "\n")
                        controlThread34[2] = 1
                        package = dataSensor3.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[2][i] = float(temp[i])
                except:
                    print("Sensor3 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor4(serial4):
    global mainPermission
    global controlThread34
    global dataSensor4
    global datas
    if(controlThread34[0] == 0): # if the first port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor4 = serial4.readline()
                except:
                    print("Sensor4 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor4 is not b''):
                        print("Sensor4 Data: " + dataSensor4.decode("utf-8") + "\n")
                        package = dataSensor4.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[3][i] = float(temp[i])
                except:
                    print("Sensor4 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread34[2] == 1 and controlThread34[3] == 0 and mainPermission):
                try:
                    dataSensor4 = serial4.readline()
                except:
                    print("Sensor4 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor4 is not b''):
                        print("Sensor4 Data: " + dataSensor4.decode("utf-8") + "\n")
                        controlThread34[3] = 1
                        package = dataSensor4.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[3][i] = float(temp[i])
                    if(controlThread34[2] == 1 and controlThread34[3] == 1):
                        controlThread34[2] = 0
                        controlThread34[3] = 0
                except:
                    print("Sensor4 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor5(serial5):
    global mainPermission
    global controlThread56
    global dataSensor5
    global datas
    if(controlThread56[1] == 0): # if the second port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor5 = serial5.readline()
                except:
                    print("Sensor5 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor5 is not b''):
                        print("Sensor5 Data: " + dataSensor5.decode("utf-8") + "\n")
                        package = dataSensor5.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[4][i] = float(temp[i])
                except:
                    print("Sensor5 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread56[2] == 0 and controlThread56[3] == 0 and mainPermission):
                try:
                    dataSensor5 = serial5.readline()
                except:
                    print("Sensor5 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor5 is not b''):
                        print("Sensor5 Data: " + dataSensor5.decode("utf-8") + "\n")
                        controlThread56[2] = 1
                        package = dataSensor5.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[4][i] = float(temp[i])
                except:
                    print("Sensor5 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor6(serial6):
    global mainPermission
    global controlThread56
    global dataSensor6
    global datas
    if(controlThread56[0] == 0): # if the first port is not opened
        while(1):
            if(mainPermission):
                try:
                    dataSensor6 = serial6.readline()
                except:
                    print("Sensor6 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor6 is not b''):
                        print("Sensor6 Data: " + dataSensor6.decode("utf-8") + "\n")
                        package = dataSensor6.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[5][i] = float(temp[i])
                except:
                    print("Sensor6 Error: Unable to read data\n")
                    continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread56[2] == 1 and controlThread56[3] == 0 and mainPermission):
                try:
                    dataSensor6 = serial6.readline()
                except:
                    print("Sensor6 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor6 is not b''):
                        print("Sensor6 Data: " + dataSensor6.decode("utf-8") + "\n")
                        controlThread56[3] = 1
                        package = dataSensor6.decode("utf-8")
                        temp = [package[i:i+9] for i in range(0, len(package), 9)]
                        for i in range(7):
                            datas[5][i] = float(temp[i])
                    if(controlThread56[2] == 1 and controlThread56[3] == 1):
                        controlThread56[2] = 0
                        controlThread56[3] = 0
                except:
                    print("Sensor6 Error: Unable to read data\n")
                    continue
            else:
                continue

def processSensor12(sensorPort1, sensorPort2): # this function is used to open the sensors
    global controlThread12
    try:
        # open the first sensor
        openedPort1 = serial.Serial(sensorPort1, baudrate=115200, timeout=0)
        controlThread12[0] = 1
    except:
        print("Sensor1 Error: No connection\n")
    
    try:
        # open the second sensor
        openedPort2 = serial.Serial(sensorPort2, baudrate=115200, timeout=0)
        controlThread12[1] = 1
    except:
        print("Sensor2 Error: No connection\n")
    
    if(controlThread12[0] == 1): # if the first sensor is opened
        # create a thread for the first sensor
        thread1 = threading.Thread(target=threadSensor1, args=(openedPort1, ))
        thread1.start()

    if(controlThread12[1] == 1): # if the second sensor is opened
        # create a thread for the second sensor
        thread2 = threading.Thread(target=threadSensor2, args=(openedPort2, ))
        thread2.start()
        thread2.join()

def processSensor34(sensorPort3, sensorPort4): # this function is used to open the sensors
    global controlThread34
    try:
        # open the first sensor
        openedPort3 = serial.Serial(sensorPort3, baudrate=115200, timeout=0)
        controlThread34[0] = 1
    except:
        print("Sensor3 Error: No connection\n")

    try:
        # open the second sensor
        openedPort4 = serial.Serial(sensorPort4, baudrate=115200, timeout=0)
        controlThread34[1] = 1
    except:
        print("Sensor4 Error: No connection\n")

    if(controlThread34[0] == 1): # if the third sensor is opened
        # create a thread for the first sensor
        thread3 = threading.Thread(target=threadSensor3, args=(openedPort3, ))
        thread3.start()

    if(controlThread34[1] == 1): # if the fourth sensor is opened
        # create a thread for the second sensor
        thread4 = threading.Thread(target=threadSensor4, args=(openedPort4, ))
        thread4.start()
        thread4.join()

def processSensor56(sensorPort5, sensorPort6): # this function is used to open the sensors
    global controlThread56
    try:
        # open the first sensor
        openedPort5 = serial.Serial(sensorPort5, baudrate=115200, timeout=0)
        controlThread56[0] = 1
    except:
        print("Sensor5 Error: No connection\n")

    try:
        # open the second sensor
        openedPort6 = serial.Serial(sensorPort6, baudrate=115200, timeout=0)
        controlThread56[1] = 1
    except:
        print("Sensor6 Error: No connection\n")

    if(controlThread56[0] == 1): # if the fifth sensor is opened
        # create a thread for the first sensor
        thread5 = threading.Thread(target=threadSensor5, args=(openedPort5, ))
        thread5.start()

    if(controlThread56[1] == 1): # if the sixth sensor is opened
        # create a thread for the second sensor
        thread6 = threading.Thread(target=threadSensor6, args=(openedPort6, ))
        thread6.start()
        thread6.join()

if __name__ == "__main__":
    # list of sensor ports
    sensorPorts = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3", "/dev/ttyACM4", "/dev/ttyACM5"]
    
    # create processes for sensors two by two.
    # each process will be having three threads.
    core1 = Process(target=processSensor12, args=(sensorPorts[0], sensorPorts[1], ))
    core2 = Process(target=processSensor34, args=(sensorPorts[2], sensorPorts[3], ))
    core3 = Process(target=processSensor56, args=(sensorPorts[4], sensorPorts[5], ))

    core1.start()
    core2.start()
    core3.start()

    '''
    core1.join()
    core2.join()
    core3.join()
    '''
    while 1:
        if controlThread12[2] == 1:
            controlThread12[4] == 0
            print("abi olctum bi de buraya geldim\n")
            controlThread12[2] = 0
            controlThread12[4] = 1