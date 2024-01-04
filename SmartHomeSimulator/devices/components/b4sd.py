
import json
import threading
import time
from datetime import datetime

from broker_settings import HOSTNAME, PORT

from paho.mqtt import publish

b4sd_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, b4sd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_b4sd_batch = b4sd_batch.copy()
            publish_data_counter = 0
            b4sd_batch.clear()
        publish.multiple(local_b4sd_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_b4sd_batch)} DB values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, b4sd_batch))
publisher_thread.daemon = True
publisher_thread.start()


def b4sd_callback(publish_event, b4sd_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    current_time = datetime.now().strftime("%H%M")
    if verbose:
        t = time.localtime()
        print(f"B4SD display {current_time} at {time.strftime('%H:%M:%S', t)}")


    payload = {
        "measurement": "B4SD",
        "simulated": b4sd_settings['simulated'],
        "runs_on": b4sd_settings["runs_on"],
        "name": b4sd_settings["name"],
        "value": current_time,
    }
    with counter_lock:
        b4sd_batch.append((b4sd_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_b4sd(settings):
    if settings['simulated']:
        from devices.actuators.b4sd import display_simulator
        display_simulator(settings)
        #b4sd_callback(publish_event, settings)
    else:
        from devices.actuators.b4sd import display
        display(settings)
        #b4sd_callback(publish_event, settings)