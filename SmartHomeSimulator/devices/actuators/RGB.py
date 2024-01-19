try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except:
    pass
from time import sleep

# disable warnings (optional)

color = "turnOff"

def led_sim():
    global color
    try:
        while True:
            if color == 'turnOff':
                print("turnOff")
            elif color == 'white':
                print("white")
            elif color == 'red':
                print("red")
            elif color == 'green':
                print("green")
            elif color == 'blue':
                print("blue")
            elif color == 'yellow':
                print("yellow")
            elif color == 'purple':
                print("purple")
            elif color == 'light_blue':
                print("light_blue")
    except KeyboardInterrupt:
        print("Error")

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

def set_color(value):
    global color
    color = value

def led(device):
    global color
    try:
        GPIO.setup(device["RED_PIN"], GPIO.OUT)
        GPIO.setup(device["GREEN_PIN"], GPIO.OUT)
        GPIO.setup(device["BLUE_PIN"], GPIO.OUT)
        while True:
            if color == 'turnOff':
                turnOff(device)
            elif color == 'white':
                white(device)
            elif color == 'red':
                red(device)
            elif color == 'green':
                green(device)
            elif color == 'blue':
                blue(device)
            elif color == 'yellow':
                yellow(device)
            elif color == 'purple':
                purple(device)
            elif color == 'light_blue':
                lightBlue(device)
    except KeyboardInterrupt:
        GPIO.cleanup()
