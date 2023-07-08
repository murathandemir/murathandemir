from multiprocessing import Process
import threading
import serial
import time

# those are variables must be declared as global. It is necessary to data exchange between threads.
dataSensor1, dataSensor2, dataSensor3, dataSensor4, dataSensor5, dataSensor6 = b'', b'', b'', b'', b'', b''


# index 1: is the port 1 opened?
# index 2: is the port 2 opened?
# index 3: has the job of the first thread done?
# index 4: has the job of the second thread done?
controlThread12 = [0, 0, 0, 0]
controlThread34 = [0, 0, 0, 0]
controlThread56 = [0, 0, 0, 0]

# 00 > 1. thread çalışır > 10 olur
# 10 > 2. thread çalışır > 11 olur
# 11 ise 00 olur.

def threadSensor1(serial1):
    global controlThread12
    global dataSensor1
    if(controlThread12[1] == 0): # if the second port != opened
        while(1):
            try:
                dataSensor1 = serial1.readline()
            except:
                print("Sensor1 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor1 != b''):
                    print("Sensor1 Data: " + dataSensor1.decode("utf-8") + "\n")
            except:
                print("Sensor1 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread12[2] == 0 and controlThread12[3] == 0):
                try:
                    dataSensor1 = serial1.readline()
                except:
                    print("Sensor1 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor1 != b''):
                        print("Sensor1 Data: " + dataSensor1.decode("utf-8") + "\n")
                        controlThread12[2] = 1
                except:
                    print("Sensor1 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor2(serial2):
    global controlThread12
    global dataSensor2
    if(controlThread12[0] == 0): # if the first port != opened
        while(1):
            try:
                dataSensor2 = serial2.readline()
            except:
                print("Sensor2 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor2 != b''):
                    print("Sensor2 Data: " + dataSensor2.decode("utf-8") + "\n")
            except:
                print("Sensor2 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread12[2] == 1 and controlThread12[3] == 0):
                try:
                    dataSensor2 = serial2.readline()
                except:
                    print("Sensor2 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor2 != b''):
                        print("Sensor2 Data: " + dataSensor2.decode("utf-8") + "\n")
                        controlThread12[3] = 1
                    if(controlThread12[2] == 1 and controlThread12[3] == 1):
                        controlThread12[2] = 0
                        controlThread12[3] = 0
                except:
                    print("Sensor2 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor3(serial3):
    global controlThread34
    global dataSensor3
    if(controlThread34[1] == 0): # if the second port != opened
        while(1):
            try:
                dataSensor3 = serial3.readline()
            except:
                print("Sensor3 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor3 != b''):
                    print("Sensor3 Data: " + dataSensor3.decode("utf-8") + "\n")
            except:
                print("Sensor3 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread34[2] == 0 and controlThread34[3] == 0):
                try:
                    dataSensor3 = serial3.readline()
                except:
                    print("Sensor3 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor3 != b''):
                        print("Sensor3 Data: " + dataSensor3.decode("utf-8") + "\n")
                        controlThread34[2] = 1
                except:
                    print("Sensor3 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor4(serial4):
    global controlThread34
    global dataSensor4
    if(controlThread34[0] == 0): # if the first port != opened
        while(1):
            try:
                dataSensor4 = serial4.readline()
            except:
                print("Sensor4 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor4 != b''):
                    print("Sensor4 Data: " + dataSensor4.decode("utf-8") + "\n")
            except:
                print("Sensor4 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread34[2] == 1 and controlThread34[3] == 0):
                try:
                    dataSensor4 = serial4.readline()
                except:
                    print("Sensor4 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor4 != b''):
                        print("Sensor4 Data: " + dataSensor4.decode("utf-8") + "\n")
                        controlThread34[3] = 1
                    if(controlThread34[2] == 1 and controlThread34[3] == 1):
                        controlThread34[2] = 0
                        controlThread34[3] = 0
                except:
                    print("Sensor4 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor5(serial5):
    global controlThread56
    global dataSensor5
    if(controlThread56[1] == 0): # if the second port != opened
        while(1):
            try:
                dataSensor5 = serial5.readline()
            except:
                print("Sensor5 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor5 != b''):
                    print("Sensor5 Data: " + dataSensor5.decode("utf-8") + "\n")
            except:
                print("Sensor5 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread56[2] == 0 and controlThread56[3] == 0):
                try:
                    dataSensor5 = serial5.readline()
                except:
                    print("Sensor5 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor5 != b''):
                        print("Sensor5 Data: " + dataSensor5.decode("utf-8") + "\n")
                        controlThread56[2] = 1
                except:
                    print("Sensor5 Error: Unable to read data\n")
                    continue
            else:
                continue

def threadSensor6(serial6):
    global controlThread56
    global dataSensor6
    if(controlThread56[0] == 0): # if the first port != opened
        while(1):
            try:
                dataSensor6 = serial6.readline()
            except:
                print("Sensor6 Error: Connection Lost. ")
                print("Retrying...\n")
                continue

            try:
                if(dataSensor6 != b''):
                    print("Sensor6 Data: " + dataSensor6.decode("utf-8") + "\n")
            except:
                print("Sensor6 Error: Unable to read data\n")
                continue
    else: # that means all the ports of related process is opened. threads must be work sequentially.
        while(1):
            if(controlThread56[2] == 1 and controlThread56[3] == 0):
                try:
                    dataSensor6 = serial6.readline()
                except:
                    print("Sensor6 Error: Connection Lost. ")
                    print("Retrying...\n")
                    continue

                try:
                    if(dataSensor6 != b''):
                        print("Sensor6 Data: " + dataSensor6.decode("utf-8") + "\n")
                        controlThread56[3] = 1
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

def SendMessage(port, message):
    port.write(message.encode("utf-8"))

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

#    core1.join()
#    core2.join()
#    core3.join()

    

