import json
import threading
import time
from broker_settings import HOSTNAME, PORT

from paho.mqtt import publish
from devices.actuators.bedroom_buzzer import turn_on_buzzer, turn_off_buzzer
db_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, db_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_db_batch = db_batch.copy()
            publish_data_counter = 0
            db_batch.clear()
        publish.multiple(local_db_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_db_batch)} DB values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, db_batch))
publisher_thread.daemon = True
publisher_thread.start()


def db_callback(publish_event, db_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    turnOn =  db_settings['turn_on']
    textTurnOn = ""
    if turnOn:
        textTurnOn = "Sound on"
    else:
        textTurnOn = "Sound off"
    if verbose:
        t = time.localtime()
        print(f"\n{textTurnOn} at {time.strftime('%H:%M:%S', t)}")

    valueTurnOn = 0
    if turnOn:
        valueTurnOn = 1

    payload = {
        "measurement": "BB",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
        "value": valueTurnOn,
    }
    with counter_lock:
        db_batch.append((db_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def handle_bb_message(payload, bb_settings):
    turnOn = payload.get("value", False)
    print("Primljena poruka",turnOn)
    if turnOn:
        turn_on_buzzer()
        run_bb(bb_settings)
    else:
        turn_off_buzzer()

def handle_bb_cancel_message(payload, bb_settings):
    turnOn = payload.get("value", False)
    print("Primljena poruka",turnOn)
    if not turnOn:
        turn_off_buzzer()



def run_bb(settings):
    if settings['simulated']:
        from devices.actuators.bedroom_buzzer import buzz, sim_buzz
        sim_buzz(settings)
        db_callback(publish_event, settings)

    else:
        from devices.actuators.bedroom_buzzer import buzz
        buzz(settings)
        db_callback(publish_event, settings)

