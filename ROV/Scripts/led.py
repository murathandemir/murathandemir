import RPi.GPIO as gpio
from time import sleep
# 12, 8, 7
gpio.setmode(gpio.BCM)
gpio.setup(12, gpio.OUT)
gpio.setup(8, gpio.OUT)
gpio.setup(7, gpio.OUT)
while True:
	# 12
    gpio.output(12, True)
    gpio.output(8, False)
    gpio.output(7, False)
    sleep(1)
	# 8
    gpio.output(8, True)
    gpio.output(12, False)
    gpio.output(7, False)
    sleep(1)
	#7
    gpio.output(7, True)
    gpio.output(8, False)
    gpio.output(12, False)
    sleep(1)
#12 - 8
    gpio.output(12, True)
    gpio.output(8, True)
    gpio.output(7, False)
    sleep(1)
#12 - 7
    gpio.output(12, True)
    gpio.output(8, False)
    gpio.output(7, True)
    sleep(1)
	#7 - 8
    gpio.output(12, False)
    gpio.output(8, True)
    gpio.output(7, True)
    sleep(1)
	#12 - 7 - 8
    gpio.output(12, True)
    gpio.output(8, True)
    gpio.output(7, True)
    sleep(1)
