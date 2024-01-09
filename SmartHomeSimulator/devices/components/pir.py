import json

from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT
import threading
import time
from devices.simulators.pir import run_pir_simulator


pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(motion, publish_event, pir_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print(
            f"\nMotion detected from {pir_settings['name']} at {time.strftime('%H:%M:%S', t)}")

    motion_payload = {
        "measurement": "Motion",
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "name": pir_settings["name"],
        "value": motion
    }

    with counter_lock:
        pir_batch.append((pir_settings['topic'], json.dumps(motion_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    publish.single(topic=pir_settings['topic_single'], payload=json.dumps(motion_payload), hostname=HOSTNAME, port=PORT)




def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        pir1_thread = threading.Thread(target=run_pir_simulator,
                                       args=(15, pir_callback, stop_event, publish_event, settings))
        pir1_thread.start()
        threads.append(pir1_thread)
        print(settings["name"] + " simulator started")
    else:
        from devices.sensors.pir import run_pir_loop, PIR
        print("Starting " + settings["name"] + " loop")
        pir = PIR(settings['pin'], settings["name"])
        pir1_thread = threading.Thread(target=run_pir_loop,
                                       args=(pir, 2, pir_callback(), stop_event, publish_event, settings))
        pir1_thread.start()
        threads.append(pir1_thread)
        print(settings["name"] + " loop started")
