#!/usr/bin/env python3

from devices.actuators.LCD.PCF8574 import PCF8574_GPIO
from devices.actuators.LCD.Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep


def loop(settings, payload):
    mcp.output(settings['pin_scl'], 1)  # turn on LCD backlight
    lcd.begin(16, settings['pin_sda'])  # set number of LCD lines and columns
    while True:
        lcd.setCursor(0, 0)  # set cursor position
        lcd.message('Temperature: ' + payload.get("temperature", False) + '\n')
        lcd.message('Humidity: ' + payload.get("humidity", False) + '\n')
        sleep(1)


def destroy():
    lcd.clear()


PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)


def display_lcd(settings, payload):
    loop(settings, payload)
