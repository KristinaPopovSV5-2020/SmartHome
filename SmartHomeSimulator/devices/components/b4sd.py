import json
import threading
from broker_settings import HOSTNAME, PORT
from paho.mqtt import publish

from devices.actuators.b4sd import turn_on_b4sd, turn_off_b4sd, set_intermittently

b4sd_thread = None


def b4sd_callback(turn_on, intermittently, b4sd_settings):
    payload = {
        "turn_on": turn_on,
        "intermittently": intermittently,
    }

    publish.single(topic=b4sd_settings['topic_single'], payload=json.dumps(payload), hostname=HOSTNAME, port=PORT)


def handle_b4sd_message(payload, b4sd_settings):
    global b4sd_thread
    try:
        print("OVDE", payload)
        intermittently = payload.get("intermittently", False)
        turnOn = payload.get("turnOn", False)
        set_intermittently(intermittently)
        if turnOn:
            turn_on_b4sd()
            if b4sd_thread is None or not b4sd_thread.is_alive():
                b4sd_thread = threading.Thread(target=run_b4sd, args=(b4sd_settings,))
                b4sd_thread.start()
        else:
            turn_off_b4sd()
        b4sd_callback(turnOn, intermittently, b4sd_settings)
    except Exception as e:
        print(f"Greška u handle_b4sd_message: {e}")


def run_b4sd(settings):
    if settings['simulated']:
        from devices.actuators.b4sd import display_simulator
        display_simulator(settings)
    else:
        from devices.actuators.b4sd import display
        display(settings)
