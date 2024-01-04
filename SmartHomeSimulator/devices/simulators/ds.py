import time
import random


def generate_press():
    while True:
        yield random.choice([True, False])


def run_ds_simulator(delay, callback, stop_event, publish_event, settings):
    pir_motion = generate_press()
    for motion in pir_motion:
        time.sleep(delay)
        callback(motion, publish_event, settings)
        if stop_event.is_set():
            break
