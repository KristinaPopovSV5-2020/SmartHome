

def handle_b4sd_message(payload, b4sd_settings):
    print("OVDE",payload)
    intermittently = payload.get("intermittently", False)
    turnOn = payload.get("turnOn", False)
    run_b4sd(b4sd_settings, intermittently, turnOn)

def run_b4sd(settings, intermittently, turnOn):
    if settings['simulated']:
        from devices.actuators.b4sd import display_simulator
        display_simulator(settings,intermittently, turnOn)
    else:
        from devices.actuators.b4sd import display
        display(settings,intermittently, turnOn)
