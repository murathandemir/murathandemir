import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(20, gpio.OUT)
while True:
    gpio.output(20, True)
    sleep(1)
    gpio.output(20, False)
    sleep(1)

# gpio 20-21-16
# 16>reset
# 20>interrupt1
# 21>interrupt2