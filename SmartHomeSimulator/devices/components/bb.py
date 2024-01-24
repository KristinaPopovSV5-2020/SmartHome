import json
import threading
import time
from broker_settings import HOSTNAME, PORT

from paho.mqtt import publish
from devices.actuators.bedroom_buzzer import turn_on_buzzer, turn_off_buzzer

bb_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()

bb_thread = None


def publisher_task(event, bb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_bb_batch = bb_batch.copy()
            publish_data_counter = 0
            bb_batch.clear()
        publish.multiple(local_bb_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_bb_batch)} BB values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bb_batch))
publisher_thread.daemon = True
publisher_thread.start()


def bb_callback(turnOn, publish_event, bb_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    if turnOn:
        textTurnOn = "Sound on"
    else:
        textTurnOn = "Sound off"
    if verbose:
        t = time.localtime()
        print(f"\nBB {textTurnOn} at {time.strftime('%H:%M:%S', t)}")

    valueTurnOn = 0
    if turnOn:
        valueTurnOn = 1

    payload = {
        "measurement": "BB",
        "simulated": bb_settings['simulated'],
        "runs_on": bb_settings["runs_on"],
        "name": bb_settings["name"],
        "value": valueTurnOn,
    }
    with counter_lock:
        bb_batch.append((bb_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def handle_bb_message(payload, bb_settings):
    global bb_thread
    try:
        turnOn = payload.get("value", False)
        if turnOn:
            turn_on_buzzer()
            if bb_thread is None or not bb_thread.is_alive():
                bb_thread = threading.Thread(target=run_bb, args=(bb_settings,))
                bb_thread.start()
        else:
            turn_off_buzzer()
        bb_callback(turnOn, publish_event, bb_settings)
    except Exception as e:
        print(f"Greška u handle_bb_message: {e}")


def run_bb(settings):
    if settings['simulated']:
        from devices.actuators.bedroom_buzzer import buzz, sim_buzz
        sim_buzz(settings)
    elif settings['jingle']:
        from devices.actuators.jingle.play import buzz
        buzz(settings)
    else:
        from devices.actuators.bedroom_buzzer import buzz
        buzz(settings)
