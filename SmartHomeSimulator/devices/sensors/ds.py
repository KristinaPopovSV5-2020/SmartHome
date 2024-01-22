import time
from functools import partial

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_ds_loop(settings, press_detected, stop_event, publish_event):
    GPIO.setup(settings['pin'], GPIO.IN)
    GPIO.add_event_detect(settings['pin'], GPIO.RISING,
                          callback=lambda channel: press_detected(True,0, publish_event, settings))
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(settings['pin'])
            break
