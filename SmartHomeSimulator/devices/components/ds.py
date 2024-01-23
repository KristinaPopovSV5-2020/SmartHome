import json

from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT
import threading
import time
from devices.simulators.ds import run_ds_simulator

ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

start_time = None
duration = 0


def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ds_batch = ds_batch.copy()
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch))
publisher_thread.daemon = True
publisher_thread.start()


def ds_callback(button_press, button_press_duration, publish_event, ds_settings, verbose=True):
    global publish_data_counter, publish_data_limit, start_time, duration

    if verbose:
        t = time.localtime()
        print(
            f"\nButton {ds_settings['name']} pressed at {time.strftime('%H:%M:%S', t)}")

    button_press_payload = {
        "measurement": "DS",
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "name": ds_settings["name"],
        "value": button_press
    }

    with counter_lock:
        ds_batch.append((ds_settings['topic'], json.dumps(button_press_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    publish.single(topic=ds_settings['topic_single'], payload=json.dumps(button_press_payload), hostname=HOSTNAME,
                   port=PORT)

    if not ds_settings['simulated']:
        if button_press:
            if start_time is None:
                start_time = time.time()
        else:
            if start_time is not None:
                duration = time.time() - start_time
                if duration > 5:
                    publish.single(topic=ds_settings['topic_duration'], payload=json.dumps(button_press_payload),
                                   hostname=HOSTNAME,
                                   port=PORT)
                start_time = None
                duration = 0

    if button_press_duration > 5 and button_press:
        publish.single(topic=ds_settings['topic_duration'], payload=json.dumps(button_press_payload), hostname=HOSTNAME,
                       port=PORT)


def run_ds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        ds1_thread = threading.Thread(target=run_ds_simulator,
                                      args=(7, ds_callback, stop_event, publish_event, settings))
        ds1_thread.start()
        threads.append(ds1_thread)
        print(settings["name"] + " simulator started")
    else:
        from devices.sensors.ds import run_ds_loop
        print("Starting " + settings["name"] + " loop")
        ds1_thread = threading.Thread(target=run_ds_loop,
                                      args=(settings, ds_callback, stop_event, publish_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print(settings["name"] + " loop started")
