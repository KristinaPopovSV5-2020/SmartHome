import json

from pynput import keyboard
import threading
from devices.components.dl import run_dl, handle_dl_message
from devices.components.db import run_db
from devices.components.pir import run_pir
from devices.components.ds import run_ds
from devices.components.dus import run_dus
from settings import load_settings
from devices.components.dht import run_dht
from devices.components.dms import run_dms
import time
import paho.mqtt.client as mqtt

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

threads = []
stop_event = threading.Event()
pi1_location = "settings/settings_PI1.json"
pi2_location = "settings/settings_PI2.json"
pi3_location = "settings/settings_PI3.json"


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic = msg.topic
    pi1_settings = load_settings("settings/settings_PI1.json")
    pi2_settings = load_settings("settings/settings_PI2.json")
    pi3_settings = load_settings("settings/settings_PI3.json")

    topic_method_mapping = {
        "server/coveredPorch/dl": handle_dl_message,
    }

    if topic in topic_method_mapping:
        topic_method_mapping[topic](payload, pi1_settings["DL"])


def mqtt_subscribe():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("server/coveredPorch/dl")
    client.loop_start()


class KeyState:
    def __init__(self):
        pi1_settings = load_settings("settings/settings_PI1.json")
        self.dl_settings = pi1_settings["DL"]
        self.db_settings = pi1_settings["DB"]

    def on_press(self, key):
        try:
            if key.char == self.dl_settings["activation"]:
                run_dl(self.dl_settings, True)
            elif key.char == self.dl_settings["activation_off"]:
                run_dl(self.dl_settings, False)
            elif key.char == self.db_settings["activation"]:
                run_db(self.db_settings, True)
            elif key.char == self.db_settings["activation_off"]:
                run_db(self.db_settings, False)

        except AttributeError:
            pass


def run_actuators():
    pi1_settings = load_settings("settings/settings_PI1.json")
    dl_settings = pi1_settings["DL"]
    db_settings = pi1_settings["DB"]
    print("If you want to turn on door light we need to press the keyboard button " + dl_settings["activation"] + " \n"
                                                                                                                  "If you want to turn off door light we need to press the keyboard button " +
          dl_settings["activation_off"])
    print("if you want to turn on door buzzer, we need to press the keyboard button " + db_settings["activation"])
    print("if you want to turn off door buzzer, we need to press the keyboard button " + db_settings["activation_off"])
    key_state = KeyState()
    with keyboard.Listener(on_press=key_state.on_press, suppress=True) as listener:
        listener.join()


def run_p1():
    pi1_settings = load_settings(pi1_location)
    ds1_settings = pi1_settings['DS1']
    run_ds(ds1_settings, threads, stop_event)

    dus1_settings = pi1_settings['DUS1']
    run_dus(dus1_settings, threads, stop_event)

    dpir1_settings = pi1_settings['DPIR1']
    run_pir(dpir1_settings, threads, stop_event)

    dms_settings = pi1_settings['DMS']
    run_dms(dms_settings, threads, stop_event)

    rpir1_settings = pi1_settings['RPIR1']
    run_pir(rpir1_settings, threads, stop_event)

    rpir2_settings = pi1_settings['RPIR2']
    run_pir(rpir2_settings, threads, stop_event)

    rdht1_settings = pi1_settings['RDHT1']
    run_dht(rdht1_settings, threads, stop_event)

    rdht2_settings = pi1_settings['RDHT2']
    run_dht(rdht2_settings, threads, stop_event)


def run_p2():
    pi2_settings = load_settings(pi2_location)


def run_p3():
    pi3_settings = load_settings(pi3_location)


if __name__ == "__main__":
    mqtt_subscribe()
    while True:
        print("Choose an option:")
        print("1. Actuators")
        print("2. Sensors")
        print("3. Exit\n\n")

        option = input("Enter the option number: ")

        if option == "1":
            run_actuators()
        elif option == "2":
            try:
                run_p1()
                run_p2()
                run_p3()
                while True:
                    time.sleep(1)

            except KeyboardInterrupt:
                print('Stopping app')
                for t in threads:
                    stop_event.set()
        elif option == "3":
            print("You have exited the program.")
            GPIO.cleanup()
            break
        else:
            print("Invalid input.")
