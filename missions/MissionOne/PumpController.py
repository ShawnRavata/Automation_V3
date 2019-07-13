from time import sleep


class PumpController:
    def __init__(self):
        pass

    def handle(self, command):
        sleep(.3)
        if command is "WITHDRAW":
            self.withdraw()
        elif command is "SLOW":
            self.slow()
        elif command is "INFUSE":
            self.infuse()

    def infuse(self):
        print("Infusing")
        # self.pump.pumping_with_delays()

    def slow(self):
        print("slowing")
        # self.pump.pumping_with_delays()

    def withdraw(self):
        print("withdrawing")
        # self.pump.pumping_with_delays()
