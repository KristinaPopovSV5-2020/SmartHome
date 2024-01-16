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

def display_simulator(device):
    current_time = datetime.now().strftime("%H%M")
    print(device['name']," display is", current_time)
    return current_time

def display(device):
    try:
        while True:
            current_time = datetime.now().strftime("%H%M")
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
    finally:
        GPIO.cleanup()
        return current_time