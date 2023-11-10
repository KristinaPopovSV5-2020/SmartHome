from DL.door_light import turn_on, turn_off
import keyboard
from settings import load_settings
import threading

from DB.door_buzzer import play_sound,stop_sound


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def handle_b_key(pin):
    if keyboard.is_pressed('B'):
        play_sound(pin)
    if not keyboard.is_pressed('B'):
        stop_sound()

if __name__ == "__main__":
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
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
            print("If you want to turn on door light we need to press the keyboard button 'O'\n"
                  "If you want to turn off door light we need to press the keyboard button 'X'\n")
            keyboard.add_hotkey('o', lambda:turn_on(dl_settings['pin']))
            keyboard.add_hotkey('x', lambda:turn_off(dl_settings['pin']))
        elif option == "3":
            print("You have selected the door ultrasonic sensor option.")
        elif option == "4":
            db_settings = settings['DB']
            print("You have selected the door buzzer option.")
            print("if you want to hear the sound, we need to hold the keyboard button 'B' \n")
            keyboard.add_hotkey('B', lambda:handle_b_key(db_settings["pin"]))
        elif option == "5":
            print("You have selected the door motion sensor option.")
        elif option == "6":
            print("You have selected the door membrane switch option.")
        elif option == "7":
            print("You have selected the room passive infrared sensor option.")

        elif option == "8":
            print("You have selected the room temperature and humidity sensor option.")

        elif option == "9":
            print("You have exited the program.")
            GPIO.cleanup()
            keyboard.unhook_all()
            break
        else:
            print("Invalid input.")