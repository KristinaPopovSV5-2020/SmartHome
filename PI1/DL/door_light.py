import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def run_dl_on(settings):
    if settings["simulated"]:
        turn_on_simulate()
    else:
        turn_on(settings["pin"])

def run_dl_off(settings):
    if settings["simulated"]:
        turn_off_simulate()
    else:
        turn_off(settings["pin"])

def turn_on(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("Light on")
    GPIO.output(pin, GPIO.HIGH)

def turn_on_simulate():
    print("Light on")


def turn_off(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("Light off")
    GPIO.output(pin, GPIO.LOW)

def turn_off_simulate():
    print("Light off")


