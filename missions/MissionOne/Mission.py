from missions.mission import Mission


class Mission(Mission):
    def __init__(self, math_controller, pump_controller):
        self.math_controller = math_controller
        self.pump_controller = pump_controller

    def handle(self, wells):
        # Withdraw Fluid
        # Slow Fluid
        # Infuse Fluid
        #
        pass
