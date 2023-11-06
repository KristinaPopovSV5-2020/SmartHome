import RPi.GPIO as GPIO
import time

LIGHT_PIN = 18


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)


def turn_on():
    print("Light on")
    GPIO.output(LIGHT_PIN, GPIO.HIGH)


def turn_off():
    print("Light off")
    GPIO.output(LIGHT_PIN, GPIO.LOW)


def cleanup_gpio():
    GPIO.cleanup()


def turn_on_ff():
    setup_gpio()
    try:
        while True:
            turn_on()
            time.sleep(5)
            turn_off()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()
