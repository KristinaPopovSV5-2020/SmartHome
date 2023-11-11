import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def buzz(pin, pitch, duration):
    print("Sound on")
    GPIO.setup(pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(pin, True)
        time.sleep(delay)
        GPIO.output(pin,False)
        time.sleep(delay)

def stop_sound():
    print("Sound off")

def run_db_on(settings):
    if settings["simulated"]:
        print("Sound on")
    else:
        buzz(settings["pin"], settings["pitch"], settings["duration"])

def run_db_off():
    stop_sound()






