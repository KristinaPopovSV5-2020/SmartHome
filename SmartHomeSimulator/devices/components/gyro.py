from paho.mqtt import publish

from devices.simulators.gyro import run_gyro_simulator
from broker_settings import HOSTNAME, PORT

import json
import time
import threading

gyro_batch = []
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
        print(f'published {publish_data_limit} GYRO values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gyro_callback(accel, gyro, publish_event, settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("AccelX: " + str(accel[0]))
        print("AccelY: " + str(accel[1]))
        print("AccelZ: " + str(accel[2]))
        print("GyroX: " + str(gyro[0]))
        print("GyroY: " + str(gyro[1]))
        print("GyroZ: " + str(gyro[2]))

    accel_payload = {
        "measurement": "Gyro",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "accel_x": accel[0],
        "accel_y": accel[1],
        "accel_z": accel[2],
        "gyro_x": gyro[0],
        "gyro_y": gyro[1],
        "gyro_z": gyro[2]
    }

    with counter_lock:
        gyro_batch.append((settings['topic'], json.dumps(accel_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        print(settings['topic'] + " publish event set")
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        gyro_thread = threading.Thread(target=run_gyro_simulator,
                                       args=(7, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(settings["name"] + " simulator started")
    else:
        from devices.sensors.gyro.gyro import run_gyro_loop
        print("Starting " + settings["name"] + " loop")
        gyro_thread = threading.Thread(target=run_gyro_loop,
                                       args=(2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(settings["name"] + " loop started")
