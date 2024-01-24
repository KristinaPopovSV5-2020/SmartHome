try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

import time
from notes import notes, load_song


def setup_active(buzzer_pin):
    GPIO.setup(buzzer_pin, GPIO.OUT)


def buzz_active(pitch, duration, buzzer_pin):
    period = 1.0 / pitch
    delay = period / 2.0
    cycles = int(duration * pitch)

    for _ in range(cycles):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(delay)


def play_active(buzzer_pin, song, duration, pause):
    global turn_on
    while True:
        for note in song:
            buzz_active(notes[note['note']], note['duration'] * duration, buzzer_pin)
            time.sleep(note['duration'] * duration * pause)
        if not turn_on:
            break

def buzz(settings):
    print('Playing: jingle.json')
    song = load_song('jingle_bells.json')
    try:
        setup_active(settings['pin'])
        play_active(settings['pin'], song, duration=0.5, pause=1)
    except KeyboardInterrupt:
        GPIO.cleanup()

    print('Performance over')
