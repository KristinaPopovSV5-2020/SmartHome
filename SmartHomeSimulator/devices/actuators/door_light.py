try:
    import RPi.GPIO as GPIO
except:
    print('Cant load')
import time

def light(turnOn, settings):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.OUT)
    if turnOn:
        GPIO.output(settings['pin'], GPIO.HIGH)

    else:
        GPIO.output(settings['pin'], GPIO.LOW)