import json

from paho.mqtt import publish

from devices.simulators.dht import run_dht_simulator
from broker_settings import HOSTNAME, PORT
import threading
import time

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} DHT values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, code, publish_event, dht_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(dht_settings["name"] + ":")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append((dht_settings['topic'] + "/temperature", json.dumps(temp_payload), 0, True))
        dht_batch.append((dht_settings['topic'] + "/humidity", json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def dht_callback_sim(humidity, temperature, publish_event, dht_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print(
            f"\n{dht_settings['name']} detected temperature: {temperature}°C and humidity: {humidity}% at {time.strftime('%H:%M:%S', t)}")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append((dht_settings['topic'] + "/temperature", json.dumps(temp_payload), 0, True))
        dht_batch.append((dht_settings['topic'] + "/humidity", json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator,
                                       args=(2, dht_callback_sim, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(settings["name"] + " sumilator started")
    else:
        from devices.sensors.dht import run_dht_loop, DHT
        print("Starting " + settings["name"] + " loop")
        dht = DHT(settings['pin'], settings["name"])
        dht1_thread = threading.Thread(target=run_dht_loop,
                                       args=(dht, 2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(settings["name"] + " loop started")
