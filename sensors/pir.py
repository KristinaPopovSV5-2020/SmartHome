import RPi.GPIO as GPIO


def run_pir_loop(PIR_PIN, motion_detected, stop_event, name):
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=lambda channel: motion_detected(name))
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(PIR_PIN)
            break
