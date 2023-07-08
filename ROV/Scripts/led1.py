import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(8, gpio.OUT)
while True:
	gpio.output(8, True)
	sleep(1)
	gpio.output(8, False)
	sleep(1)
