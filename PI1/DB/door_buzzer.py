import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass





def buzz(pin,pitch, duration):
    GPIO.setup(pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(pin, True)
        time.sleep(delay)
        GPIO.output(pin, False)
        time.sleep(delay)



