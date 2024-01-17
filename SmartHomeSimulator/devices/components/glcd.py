import json
import threading
import time
from broker_settings import HOSTNAME, PORT

from paho.mqtt import publish



def handle_lcd_message(payload, lcd_settings):
    print("RADI SEV")
    run_lcd(lcd_settings)


def run_lcd(settings):
    if settings['simulated']:
        print("DA")
        #nesto
    else:
        from devices.actuators.LCD.LCD1602 import display_lcd
        display_lcd(settings)
