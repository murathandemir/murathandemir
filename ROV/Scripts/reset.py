import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.OUT)
gpio.output(16, False)
sleep(1)
gpio.output(16, True)
