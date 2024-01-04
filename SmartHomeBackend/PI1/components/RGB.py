def run_b4sd(settings):
    if settings['simulated']:

        print("Nesto")
    else:
        from PI1.actuators.RGB import led
        led(settings)