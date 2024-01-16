import json

import threading
from devices.components.dl import handle_dl_message
from devices.components.db import handle_db_message
from devices.components.pir import run_pir
from devices.components.ds import run_ds
from devices.components.dus import run_dus
from devices.components.bir import run_bir
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
        "server/pi1/coveredPorch/dl": handle_dl_message,
        "server/pi1/foyer/db": handle_db_message,
    }

    pi_device = topic.split("/")[1]
    device = topic.split("/")[3].upper()

    if topic in topic_method_mapping:
        if pi_device == "pi1":
            topic_method_mapping[topic](payload, pi1_settings[device])
        elif pi_device == "pi2":
            topic_method_mapping[topic](payload, pi2_settings[device])
        elif pi_device == "pi3":
            topic_method_mapping[topic](payload, pi3_settings[device])


def mqtt_subscribe():
    client = mqtt.Client()
    client.on_message = on_message
    #client.connect("10.1.121.34", 1883, 60)
    client.connect("localhost", 1883, 60)
    client.subscribe("server/pi1/coveredPorch/dl")
    client.subscribe("server/pi1/foyer/db")
    client.loop_start()


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

    rpir4_settings = pi3_settings['RPIR4']
    run_pir(rpir4_settings, threads, stop_event)

    rdht4_settings = pi3_settings['RDHT4']
    run_dht(rdht4_settings, threads, stop_event)

    bir_settings = pi3_settings['BIR']
    run_bir(bir_settings, threads, stop_event)

if __name__ == "__main__":
    mqtt_subscribe()

    try:
        run_p1()
        run_p2()
        run_p3()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        GPIO.cleanup()
        for t in threads:
            stop_event.set()
