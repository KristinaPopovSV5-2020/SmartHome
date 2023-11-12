import time
import random


def generate_values():
    buttons = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', '*', '#'}
    while True:
        yield random.choice(list(buttons))


def run_dms_simulator(delay, callback, stop_event, name):
    for code in generate_values():
        time.sleep(delay)
        callback(code, name)
        if stop_event.is_set():
            break