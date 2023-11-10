import time
import random


def generate_distance():
    distance = 50
    while random.choice([True, False]):
        distance += random.randint(-10, 10)
        if distance < 10:
            distance = 10
        yield distance


def run_dus_simulator(delay, callback, stop_event, name):
    dus_distance = generate_distance()
    for distance in dus_distance:
        time.sleep(delay)
        callback(name, distance)
        if stop_event.is_set():
            break
