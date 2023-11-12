import pyautogui
from pynput import keyboard
import threading
from PI1.DB.door_buzzer import run_db_on, run_db_off
from PI1.DL.door_light import run_dl_on,run_dl_off
from PI1.components.pir import run_pir
from PI1.components.ds import run_ds
from PI1.components.dus import run_dus
from settings import load_settings
from PI1.components.dht import run_dht
from PI1.components.dms import run_dms
import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

class KeyState:
    def __init__(self):
        pi1_settings = load_settings("settings.json")
        self.dl_settings = pi1_settings["DL"]
        self.db_settings = pi1_settings["DB"]

    def on_press(self, key):
        try:
            if key.char == self.dl_settings["activation"]:
                run_dl_on(self.dl_settings)
            elif key.char == self.dl_settings["activation_off"]:
                run_dl_off(self.dl_settings)
            elif key.char == self.db_settings["activation"]:
                run_db_on(self.db_settings)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == self.db_settings["activation"]:
                run_db_off()
        except AttributeError:
            pass



def run_actuators():
    pi1_settings = load_settings("settings.json")
    dl_settings = pi1_settings["DL"]
    db_settings = pi1_settings["DB"]
    print("If you want to turn on door light we need to press the keyboard button " + dl_settings["activation"] + " \n"
    "If you want to turn off door light we need to press the keyboard button " +
          dl_settings["activation_off"])
    print("if you want to hear the sound, we need to hold the keyboard button " + db_settings["activation"] + " \n")
    key_state = KeyState()
    with keyboard.Listener(on_press=key_state.on_press, on_release=key_state.on_release,suppress=True) as listener:
        listener.join()


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
