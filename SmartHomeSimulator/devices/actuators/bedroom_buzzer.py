import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


turn_on = False


def turn_on_buzzer():
    global turn_on
    turn_on = True


def turn_off_buzzer():
    global turn_on
    turn_on = False
    print("ISKLJ", turn_on)

def sim_buzz(settings):
    while True:
        print("Cuje se", turn_on)
        if not turn_on:
            break
        time.sleep(2)
    print("Ne cuje se")

def buzz(settings):
    pin = settings['pin']
    GPIO.setup(pin, GPIO.OUT)
    pitch = settings['pitch']
    duration = settings['duration']
    period = 1.0 / pitch
    delay = period / 2

    while turn_on:
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(pin, True)
            time.sleep(delay)
            GPIO.output(pin, False)
            time.sleep(delay)

    GPIO.output(pin, False)
