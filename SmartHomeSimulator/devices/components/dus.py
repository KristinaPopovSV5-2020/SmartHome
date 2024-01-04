import json

from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT
import threading
import time
from devices.simulators.dus import run_dus_simulator


dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dus_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dus_batch = dus_batch.copy()
            publish_data_counter = 0
            dus_batch.clear()
        publish.multiple(local_dus_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dus values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(distance, code, publish_event, dus_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(dus_settings["name"] + ":")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: {distance}%")

    distance_payload = {
        "measurement": "DUS",
        "simulated": dus_settings['simulated'],
        "runs_on": dus_settings["runs_on"],
        "name": dus_settings["name"],
        "value": distance
    }

    with counter_lock:
        dus_settings.append((dus_settings['topic'], json.dumps(distance_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def dus_callback_sim(distance, publish_event, dht_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print(
            f"\nUltranosic sensor {dht_settings['name']} detected movement from " + str(distance) + f"cm at {time.strftime('%H:%M:%S', t)}")

    distance_payload = {
        "measurement": "DUS",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": distance
    }

    with counter_lock:
        dus_batch.append((dht_settings['topic'], json.dumps(distance_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        dus1_thread = threading.Thread(target=run_dus_simulator, args=(2, dus_callback_sim, stop_event, publish_event, settings))
        dus1_thread.start()
        threads.append(dus1_thread)
        print(settings["name"] + " simulator started")
    else:
        from devices.sensors.dus import run_dus_loop, DUS
        print("Starting " + settings["name"] + " loop")
        dus = DUS(settings['pin'], settings["name"])
        dus1_thread = threading.Thread(target=run_dus_loop,
                                       args=(dus, 2, dus_callback, stop_event, publish_event, settings))
        dus1_thread.start()
        threads.append(dus1_thread)
        print(settings["name"] + " loop started")
