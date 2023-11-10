from DL.door_light import turn_on, turn_off
import keyboard
from settings import load_settings


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    settings = load_settings()
    threads = []
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
            break
        else:
            print("Invalid input.")