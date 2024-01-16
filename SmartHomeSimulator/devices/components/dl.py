import json
import threading
import time
from broker_settings import HOSTNAME, PORT
from paho.mqtt import publish

dl_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_dl_batch)} DL values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dl_callback(turnOn, publish_event, dl_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    if turnOn:
        textTurnOn = "Light on"
    else:
        textTurnOn = "Light off"
    if verbose:
        t = time.localtime()
        print(f"\n{textTurnOn} at {time.strftime('%H:%M:%S', t)}")

    valueTurnOn = 0
    if turnOn:
        valueTurnOn = 1

    payload = {
        "measurement": "DL",
        "simulated": dl_settings['simulated'],
        "runs_on": dl_settings["runs_on"],
        "name": dl_settings["name"],
        "value": valueTurnOn,
    }
    with counter_lock:
        dl_batch.append((dl_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def handle_dl_message(payload, dl_settings):
    print("Svetlo se uplaio")
    turn_on = payload.get("value", False)
    run_dl(dl_settings, turn_on)


def run_dl(settings, turnOn):
    if settings['simulated']:
        dl_callback(turnOn, publish_event, settings)
    else:
        from devices.actuators.door_light import light
        light(turnOn, settings)
        dl_callback(turnOn, publish_event, settings)
