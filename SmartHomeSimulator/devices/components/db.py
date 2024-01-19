import json
import threading
import time
from broker_settings import HOSTNAME, PORT

from paho.mqtt import publish

from devices.actuators.door_buzzer import turn_on_buzzer, turn_off_buzzer

db_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()

db_thread = None
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


def db_callback(turnOn,publish_event, db_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    textTurnOn = ""
    if turnOn:
        textTurnOn = "Sound on"
    else:
        textTurnOn = "Sound off"
    if verbose:
        t = time.localtime()
        print(f"\nDB {textTurnOn} at {time.strftime('%H:%M:%S', t)}")

    valueTurnOn = 0
    if turnOn:
        valueTurnOn = 1

    payload = {
        "measurement": "DB",
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


def handle_db_message(payload, db_settings):
    global db_thread
    try:
        turnOn = payload.get("value", False)
        if turnOn:
            turn_on_buzzer()
            if db_thread is None or not db_thread.is_alive():
                db_thread = threading.Thread(target=run_db, args=(db_settings,))
                db_thread.start()
        else:
            turn_off_buzzer()
        db_callback(turnOn, publish_event, db_settings)
    except Exception as e:
        print(f"Greška u handle_db_message: {e}")


def run_db(settings):
    if settings['simulated']:
        from devices.actuators.door_buzzer import buzz, sim_buzz
        sim_buzz(settings)
    else:
        from devices.actuators.door_buzzer import buzz
        buzz(settings)

