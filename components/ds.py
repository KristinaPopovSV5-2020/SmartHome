import threading
import time
from simulators.ds import run_ds_simulator

def ds_callback(motion_detected, name):
    t = time.localtime()
    if motion_detected:
        print("\nButton " + name + f" pressed at {time.strftime('%H:%M:%S', t)}")


def run_ds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(2, ds_callback, stop_event, settings["name"]))
        ds_thread.start()
        threads.append(ds_thread)
        print(settings["name"] + " simulator started")
    else:
        from sensors.ds import run_ds_loop
        print("Starting " + settings["name"] + " loop")
        ds_thread = threading.Thread(target=run_ds_loop, args=(settings["pin"], ds_callback, stop_event, settings["name"]))
        ds_thread.start()
        threads.append(ds_thread)
        print(settings["name"] + " loop started")