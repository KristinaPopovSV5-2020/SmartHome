import RPi.GPIO as GPIO
import time



BUZZER_PIN = 17


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, True)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, False)
        time.sleep(delay)

def cleanup_gpio():
    GPIO.cleanup()

def emit_sound(pitch,duration):
    try:
        while True:
            buzz(pitch, duration)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()

