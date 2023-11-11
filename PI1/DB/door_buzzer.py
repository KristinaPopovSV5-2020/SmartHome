import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def buzz(pin, pitch, duration):
    print("Sound on")
    #GPIO.setup(pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        #GPIO.output(pin, True)
        time.sleep(delay)
        #GPIO.output(pin,False)
        time.sleep(delay)

def play_sound(pin):
    buzz(pin, 440, 0.1)

def stop_sound():
    print("Sound off")




