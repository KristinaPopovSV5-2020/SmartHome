import keyboard
import threading
from PI1.DL.door_light import turn_on, turn_off
from components.pir import run_pir
from settings import load_settings

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    pi1_settings = load_settings("settings.json")
    dpir1_settings = pi1_settings['DPIR1']
    rpir1_settings = pi1_settings['RPIR1']
    rpir2_settings = pi1_settings['RPIR2']
    while True:
        print("Choose an option:")
        print("1. Door sensor")
        print("2. Door light")
        print("3. Door ultrasonic sensor")
        print("4. Door buzzer")
        print("5. Door motion sensor")
        print("6. Door membrane switch")
        print("7. Room passive infrared sensor")
        print("8. Room temperature and humidity sensor")
        print("9. Exit\n\n")

        option = input("Enter the option number: ")

        if option == "1":
            print("You have selected the door sensor option.")

        elif option == "2":
            dl_settings = settings['DL']
            print("You have selected the door light option.")
            print("If you want to turn on door light we need to press the keyboard button 'o',"
                  "If you want to turn off door light we need to press the keyboard button 'x'")
            keyboard.add_hotkey('o', turn_on(dl_settings['pin']))
            keyboard.add_hotkey('x', turn_off(dl_settings['pin']))
        elif option == "3":
            print("You have selected the door ultrasonic sensor option.")
        elif option == "4":
            db_settings = settings['DL']
            print("You have selected the door buzzer option.")

        elif option == "5":
            run_pir(dpir1_settings, threads, stop_event)
        elif option == "6":
            print("You have selected the door membrane switch option.")
        elif option == "7":
            run_pir(rpir1_settings, threads, stop_event)
            run_pir(rpir2_settings, threads, stop_event)

        elif option == "8":
            print("You have selected the room temperature and humidity sensor option.")

        elif option == "9":
            print("You have exited the program.")
            GPIO.cleanup()
            break
        else:
            print("Invalid input.")
