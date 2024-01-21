def handle_lcd_message(payload, lcd_settings):
    run_lcd(lcd_settings, payload)


def run_lcd(settings, payload):
    if settings['simulated']:
        print("DA")
        # nesto
    else:
        from devices.actuators.LCD.LCD1602 import display_lcd
        display_lcd(settings, payload)
