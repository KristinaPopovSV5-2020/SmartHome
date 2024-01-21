import random
import time


def generate_accel_gyro():
    accel = [0, 0, 0]
    gyro = [0, 0, 0]
    while True:
        accel = [min(2, max(-2, a + random.uniform(-0.05, 0.05))) for a in accel]
        gyro = [min(250, max(-250, g + random.uniform(-5, 5))) for g in gyro]
        yield accel, gyro


def run_gyro_simulator(delay, callback, stop_event, publish_event, settings):
    accel_gyro_generator = generate_accel_gyro()
    while True:
        accel, gyro = next(accel_gyro_generator)
        callback(accel, gyro, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
