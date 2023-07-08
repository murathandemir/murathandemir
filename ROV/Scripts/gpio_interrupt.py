import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(20, gpio.OUT)

gpio.output(20, True)
sleep(1)
gpio.output(20, False)

