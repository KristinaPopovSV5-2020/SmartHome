try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_pir_loop(settings, motion_detected, stop_event, publish_event):
    GPIO.setup(settings['pin'], GPIO.IN)
    GPIO.add_event_detect(settings['pin'], GPIO.RISING, callback=lambda channel: motion_detected(True, publish_event, settings))
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(settings['pin'])
            break
