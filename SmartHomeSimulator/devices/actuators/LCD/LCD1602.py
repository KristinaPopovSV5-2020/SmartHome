#!/usr/bin/env python3

from devices.actuators.LCD.PCF8574 import PCF8574_GPIO
from devices.actuators.LCD.Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep

temperature_value = ""
humidity_value = ""


def loop(settings, payload):
    global temperature_value, humidity_value
    mcp.output(settings['pin_scl'], 1)
    lcd.begin(16, settings['pin_sda'])
    while True:
        lcd.setCursor(0, 0)  # set cursor position
        lcd.message('Temperature: ' + temperature_value + '\n')
        lcd.message('Humidity: ' + humidity_value + '\n')
        sleep(1)


def destroy():
    lcd.clear()


PCF8574_address = 0x27
PCF8574A_address = 0x3F
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error !')
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)


def display_lcd(settings, payload):
    global temperature_value, humidity_value
    if payload.get("temperature", ""):
        temperature_value = str(payload.get("temperature", ""))
    if payload.get("humidity", ""):
        humidity_value = str(payload.get("humidity", ""))
    loop(settings, payload)
