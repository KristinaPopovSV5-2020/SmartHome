import json
import threading
import time
from broker_settings import HOSTNAME, PORT
from paho.mqtt import publish

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_rgb_batch)} RGB values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(color, publish_event, rgb_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        print(f"\n{color} light at {time.strftime('%H:%M:%S', t)}")

    payload = {
        "measurement": "RGB",
        "simulated": rgb_settings['simulated'],
        "runs_on": rgb_settings["runs_on"],
        "name": rgb_settings["name"],
        "value": color,
    }
    with counter_lock:
        rgb_batch.append((rgb_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def handle_brgb_message(payload, rgb_settings):
    color = payload.get("color", None)
    if color != ' ':
        run_brgb(rgb_settings, color)


def run_brgb(settings, color):
    if settings['simulated']:
        rgb_callback(color, publish_event, settings)
    else:
        from devices.actuators.RGB import led
        led(settings, color)
        rgb_callback(color, publish_event, settings)
