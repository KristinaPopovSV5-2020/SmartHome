import time
from datetime import datetime

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}

turn_on = False
intermittently = False


def turn_on_b4sd():
    global turn_on
    turn_on = True


def turn_off_b4sd():
    global turn_on
    turn_on = False

def set_intermittently(value):
    global intermittently
    intermittently = value



def display_simulator(device):
    global turn_on, intermittently
    current_time = datetime.now().strftime("%H:%M")
    while True:
        print(device['name'], " display is", current_time)
        if intermittently:
            time.sleep(0.5)
        if not turn_on:
            break
    print(device['name'], " does not display.")


def display(device):
    global turn_on, intermittently
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M")
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(device["segments"][loop], num[current_time[digit]][loop])
                if digit == 1 and datetime.now().second % 2 == 0:
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
                GPIO.output(device["digits"][digit], 0)
                time.sleep(0.001)
                GPIO.output(device["digits"][digit], 1)
            if intermittently:
                time.sleep(0.5)
            if not turn_on:
                break
    finally:
        GPIO.cleanup()
