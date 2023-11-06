from DL.door_light import turn_on_ff
from DB.door_buzzer import emit_sound

if __name__ == "__main__":
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


        # Korisnik unosi izbor
        option = input("Enter the option number: ")

        if option == "1":
            print("You've selected the door sensor option.")

        elif option == "2":
            print("You've selected the door light option.")
            turn_on_ff()
        elif option == "3":
            print("You've selected the door ultrasonic sensor option.")
        elif option == "4":
            print("You've selected the door buzzer option.")
            while True:
                pitch_s = input("Enter the pitch: ")
                if pitch_s.isdigit():
                    pitch = int(pitch_s)
                    break
                else:
                    print("This is not a number.")
            while True:
                duration_s = input("Enter the duration: ")
                if duration_s.replace('.', '', 1).isdigit() and duration_s.count('.') <= 1:
                    duration = float(duration_s)
                    break
                else:
                    print("This is not a number.")
            emit_sound(pitch, duration)
        elif option == "5":
            print("You've selected the door motion sensor option.")
        elif option == "6":
            print("You've selected the door membrane switch option.")
        elif option == "7":
            print("You've selected the room passive infrared sensor option.")

        elif option == "8":
            print("You've selected the room temperature and humidity sensor.")

        elif option == "9":
            print("You have exited the program.")
            break
        else:
            print("Invalid input.")