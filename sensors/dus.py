import time
import RPi.GPIO as GPIO


def get_distance(TRIG_PIN, ECHO_PIN):
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

    iter = 0
    while GPIO.input(ECHO_PIN) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(ECHO_PIN) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2
    return distance


def run_dus_loop(TRIG_PIN, ECHO_PIN, callback, stop_event, name):
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    while True:
        distance = get_distance(TRIG_PIN, ECHO_PIN)
        if distance is not None:
            callback(name, distance)
            print(f'Distance: {distance} cm')
        else:
            print('Measurement timed out')
        time.sleep(1)
        if stop_event.is_set():
            break
