try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_ds_loop(DS_PIN, press_detected, stop_event, name):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(DS_PIN, GPIO.RISING, callback=lambda channel: press_detected(name), bouncetime=100)
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(DS_PIN)
            break