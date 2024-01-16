import time
import random
def generate_values():
    buttons = {"LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"}
    while True:
        yield random.choice(list(buttons))


def run_bir_simulator(delay, callback, stop_event, publish_event, settings):
    for code in generate_values():
        time.sleep(delay)
        callback(code, publish_event, settings)
        if stop_event.is_set():
            break