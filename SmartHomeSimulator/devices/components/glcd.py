def handle_lcd_message(payload, lcd_settings):
    run_lcd(lcd_settings, payload)


def run_lcd(settings, payload):
    if settings['simulated']:
        if payload.get("temperature", False):
            print('LCD: Temperature: ' + str(payload.get("temperature", False)) + '\n')
        if payload.get("humidity", False):
            print('LCD: Humidity: ' + str(payload.get("humidity", False)) + '\n')
    else:
        from devices.actuators.LCD.LCD1602 import display_lcd
        display_lcd(settings, payload)
