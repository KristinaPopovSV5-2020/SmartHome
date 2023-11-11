import pyautogui
import threading
from PI1.DB.door_buzzer import play_sound, stop_sound
from PI1.DL.door_light import turn_on, turn_off
from PI1.components.pir import run_pir
from PI1.components.ds import run_ds
from PI1.components.dus import run_dus
from settings import load_settings
from PI1.components.dht import run_dht
import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_actuators():
    print("If you want to turn on door light we need to press the keyboard button 'O'\n"
          "If you want to turn off door light we need to press the keyboard button 'X'\n")
    print("if you want to hear the sound, we need to hold the keyboard button 'B' \n")
    pass

def run_sensors():
    threads = []
    stop_event = threading.Event()
    pi1_settings = load_settings("settings.json")
    try:
        ds1_settings = pi1_settings['DS1']
        run_ds(ds1_settings, threads, stop_event)

        dus1_settings = pi1_settings['DUS1']
        run_dus(dus1_settings, threads, stop_event)

        dpir1_settings = pi1_settings['DPIR1']
        run_pir(dpir1_settings, threads, stop_event)

        rpir1_settings = pi1_settings['RPIR1']
        run_pir(rpir1_settings, threads, stop_event)

        rpir2_settings = pi1_settings['RPIR2']
        run_pir(rpir2_settings, threads, stop_event)

        rdht1_settings = pi1_settings['RDHT1']
        run_dht(rdht1_settings, threads, stop_event)

        rdht2_settings = pi1_settings['RDHT2']
        run_dht(rdht2_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()



if __name__ == "__main__":
    while True:
        print("Choose an option:")
        print("1. Actuators")
        print("2. Sensors")
        print("3. Exit\n\n")

        option = input("Enter the option number: ")

        if option == "1":
            run_actuators()
        elif option == "2":
            run_sensors()
        elif option == "3":
            print("You have exited the program.")
            GPIO.cleanup()
            break
        else:
            print("Invalid input.")
