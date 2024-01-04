import time
import random


def generate_distance():
    distance = 50
    while True:
        distance += random.randint(-10, 10)
        if distance < 10:
            distance = 10
        yield distance


def run_dus_simulator(delay, callback, stop_event, publish_event, settings):
    for distance in generate_distance():
        time.sleep(delay)
        callback(distance, publish_event, settings)
        if stop_event.is_set():
            break
