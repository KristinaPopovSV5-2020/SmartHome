import threading
import time
from PI1.simulators.pir import run_pir_simulator


def pir_callback(motion_detected, name):
    t = time.localtime()
    if motion_detected:
        print("\nMotion detected from " + name + f" at {time.strftime('%H:%M:%S', t)}")


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings["name"]))
        pir_thread.start()
        threads.append(pir_thread)
        print(settings["name"] + " simulator started")
    else:
        from PI1.sensors.pir import run_pir_loop
        print("Starting " + settings["name"] + " loop")
        pir_thread = threading.Thread(target=run_pir_loop, args=(settings["pin"], pir_callback, stop_event, settings["name"]))
        pir_thread.start()
        threads.append(pir_thread)
        print(settings["name"] + " loop started")
