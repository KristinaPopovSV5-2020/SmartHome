

from PI1.simulators.dht import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code, name):
    t = time.localtime()
    print("="*20)
    print(name + ":")
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")

def dht_callback_sim(humidity, temperature,name):
    t = time.localtime()
    print(f"\n{name} detected temperature: {temperature}°C and humidity: {humidity}% at {time.strftime('%H:%M:%S', t)}")



def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting " + settings["name"] + " similator")
            dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback_sim, stop_event, settings["name"]))
            dht1_thread.start()
            threads.append(dht1_thread)
            print(settings["name"] + " sumilator started")
        else:
            from PI1.sensors.dht import run_dht_loop, DHT
            print("Starting " + settings["name"] + " loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, settings["name"]))
            dht1_thread.start()
            threads.append(dht1_thread)
            print(settings["name"] + " loop started")
