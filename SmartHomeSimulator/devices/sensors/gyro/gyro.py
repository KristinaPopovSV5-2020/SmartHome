#!/usr/bin/env python3
import MPU6050
import time
import os

mpu = MPU6050.MPU6050()
accel = [0] * 3
gyro = [0] * 3


def setup():
    mpu.dmp_initialize()


def run_gyro_loop(delay, callback, stop_event, publish_event, settings):
    setup()
    while True:
        accel = mpu.get_acceleration()  # AccelerationX, Y, Z
        gyro = mpu.get_rotation()  # RotationX, Y, Z
        callback(accel, gyro, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
