from PI1.simulators.dms import run_dms_simulator
import threading
import time


def dms_callback(code, name):
    t = time.localtime()
    print(f"\n{name} detected code: {code} at {time.strftime('%H:%M:%S', t)}")


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " similator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, settings["name"]))
        dms_thread.start()
        threads.append(dms_thread)
        print(settings["name"] + " sumilator started")
    else:
        from PI1.sensors.dms import run_dms_loop, DMS
        print("Starting " + settings["name"] + " loop")
        dms = DMS(settings["R1"], settings["R2"], settings["R3"], settings["R4"], settings["C1"], settings["C2"],
                  settings["C3"], settings["C4"], settings["name"])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event, settings["name"]))
        dms_thread.start()
        threads.append(dms_thread)
        print(settings["name"] + " loop started")
