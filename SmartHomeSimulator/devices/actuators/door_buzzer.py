import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def buzz(settings, turnOn):
    if turnOn:
        pin = settings['pin']
        GPIO.setup(pin, GPIO.OUT)
        pitch = settings['pitch']
        duration = settings['duration']
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(pin, True)
            time.sleep(delay)
            GPIO.output(pin, False)
            time.sleep(delay)







