import json

from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT

from devices.simulators.dms import run_dms_simulator
import threading
import time




dms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dms_batch = dms_batch.copy()
            publish_data_counter = 0
            dms_batch.clear()
        publish.multiple(local_dms_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_dms_batch)} DMS values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dms_callback(code, publish_event, dms_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        print(f"\n{dms_settings['name']} detected code: {code} at {time.strftime('%H:%M:%S', t)}")

    payload = {
        "measurement": "DMS",
        "simulated": dms_settings['simulated'],
        "runs_on": dms_settings["runs_on"],
        "name": dms_settings["name"],
        "value": code,
    }

    with counter_lock:
        # Objavljivanje podataka u okviru "home/dht" topika
        dms_batch.append((dms_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, publish_event, settings))
        dms_thread.start()
        threads.append(dms_thread)
        print(settings["name"] + " sumilator started")
    else:
        from devices.sensors.dms import run_dms_loop, DMS
        print("Starting " + settings["name"] + " loop")
        dms = DMS(settings["R1"], settings["R2"], settings["R3"], settings["R4"], settings["C1"], settings["C2"],
                  settings["C3"], settings["C4"], settings["name"])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event, publish_event, settings))
        dms_thread.start()
        threads.append(dms_thread)
        print(settings["name"] + " loop started")
