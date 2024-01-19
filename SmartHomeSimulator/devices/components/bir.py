import json
from devices.simulators.bir import run_bir_simulator
from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT

import threading
import time

bir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, bir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_bir_batch = bir_batch.copy()
            publish_data_counter = 0
            bir_batch.clear()
        publish.multiple(local_bir_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_bir_batch)} BIR values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch))
publisher_thread.daemon = True
publisher_thread.start()


def bir_callback(code, publish_event, bir_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        print(f"\n{bir_settings['name']} detected code: {code} at {time.strftime('%H:%M:%S', t)}")

    payload = {
        "measurement": "BIR",
        "simulated": bir_settings['simulated'],
        "runs_on": bir_settings["runs_on"],
        "name": bir_settings["name"],
        "value": code,
    }

    with counter_lock:
        # Objavljivanje podataka u okviru "home/dht" topika
        bir_batch.append((bir_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    publish.single(topic=bir_settings['turn_on_rgb_topic'], payload=json.dumps(payload), hostname=HOSTNAME, port=PORT)


def handle_bir_message(payload, rgb_settings):
    code = payload.get("code", " ")
    if rgb_settings['simulated']:
        run_bir_sim(rgb_settings, code)


def run_bir_sim(rgb_settings, code):
    bir_callback(code, publish_event, rgb_settings)


def run_bir(settings, threads, stop_event):
    if not settings['simulated']:
        from devices.sensors.bir import run_bir_loop
        print("Starting " + settings["name"] + " loop")
        bir_thread = threading.Thread(target=run_bir_loop, args=(bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        print(settings["name"] + " loop started")
    """if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        bir_thread = threading.Thread(target=run_bir_simulator, args=(2, bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        print(settings["name"] + " sumilator started")"""
