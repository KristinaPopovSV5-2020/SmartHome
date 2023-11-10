import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass



def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        #GPIO.output(BUZZER_PIN, True)
        time.sleep(delay)
        #GPIO.output(BUZZER_PIN, False)
        time.sleep(delay)



