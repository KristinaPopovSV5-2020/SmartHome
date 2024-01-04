def run_b4sd(settings):
    if settings['simulated']:

        print("Nesto")
    else:
        from devices.actuators.RGB import led
        led(settings)