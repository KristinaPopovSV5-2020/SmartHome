try:
    import RPi.GPIO as GPIO
except:
    print('Cant load')
import time

def light(turnOn, settings):
    pin = settings['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    if turnOn:
        GPIO.output(pin, GPIO.HIGH)

    else:
        GPIO.output(pin, GPIO.LOW)