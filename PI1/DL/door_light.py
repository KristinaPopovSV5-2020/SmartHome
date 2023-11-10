import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def turn_on(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("Light on")
    GPIO.output(pin, GPIO.HIGH)


def turn_off(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("Light off")
    GPIO.output(pin, GPIO.LOW)


