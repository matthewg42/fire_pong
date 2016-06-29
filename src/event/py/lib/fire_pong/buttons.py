
def get_buttons(config):
    if config['buttons']['use'] == 'simbuttons':
        from fire_pong.simbuttons import SimButtons
        buttons = SimButtons(config)
        return buttons
    elif config['buttons']['use'] == 'gpiobuttons':
        from fire_pong.gpiobuttons import GPioButtons
        buttons = GpioButtons(config)
        return buttons
        
