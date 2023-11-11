import time
try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

class DMS(object):
    R1 = 25
    R2 = 8
    R3 = 7
    R4 = 1

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_line(self,line, characters):
        GPIO.output(line, GPIO.HIGH)
        try:
            if GPIO.input(self.C1) == 1:
                return characters[0]
            if GPIO.input(self.C2) == 1:
                return characters[1]
            if GPIO.input(self.C3) == 1:
                return characters[2]
            if GPIO.input(self.C4) == 1:
                return characters[3]
        finally:
            GPIO.output(line, GPIO.LOW)

def extract_non_none_value(values):
    for value in values:
        if value is not None:
            return value
    return None


def run_dms_loop(dms,delay, callback, stop_event, name):
    dms.setup_gpio()
    while True:
        values = (
            dms.read_line(dms.R1, ["1", "2", "3", "A"]),
            dms.read_line(dms.R2, ["4", "5", "6", "B"]),
            dms.read_line(dms.R3, ["7", "8", "9", "C"]),
            dms.read_line(dms.R4, ["*", "0", "#", "D"])
        )
        code = extract_non_none_value(values)
        if code is not None:
            callback(code, name)
        if stop_event.is_set():
            break
        time.sleep(delay)