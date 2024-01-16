try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass
from time import sleep

# disable warnings (optional)
GPIO.setwarnings(False)



def turnOff(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def white(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def red(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def green(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def blue(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def yellow(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def purple(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def lightBlue(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def led(device):
    try:
        GPIO.setup(device["RED_PIN"], GPIO.OUT)
        GPIO.setup(device["GREEN_PIN"], GPIO.OUT)
        GPIO.setup(device["BLUE_PIN"], GPIO.OUT)
        while True:
            turnOff(device)
            sleep(1)
            white(device)
            sleep(1)
            red(device)
            sleep(1)
            green(device)
            sleep(1)
            blue(device)
            sleep(1)
            yellow(device)
            sleep(1)
            purple(device)
            sleep(1)
            lightBlue(device)
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
