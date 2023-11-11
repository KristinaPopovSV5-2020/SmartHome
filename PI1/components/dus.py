import threading
import time
from PI1.simulators.dus import run_dus_simulator


def dus_callback(name, distance):
    t = time.localtime()
    print("\nUltranosic sensor " + name + " detected movement from " + str(distance) + f"cm at {time.strftime('%H:%M:%S', t)}")


def run_dus(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        dus_thread = threading.Thread(target=run_dus_simulator, args=(2, dus_callback, stop_event, settings["name"]))
        dus_thread.start()
        threads.append(dus_thread)
        print(settings["name"] + " simulator started")
    else:
        from PI1.sensors.dus import run_dus_loop
        print("Starting " + settings["name"] + " loop")
        dus_thread = threading.Thread(target=run_dus_loop,
                                      args=(settings["pin_trig"], settings["pin_echo"], dus_callback, stop_event, settings["name"]))
        dus_thread.start()
        threads.append(dus_thread)
        print(settings["name"] + " loop started")
