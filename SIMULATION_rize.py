import time

class Rize:
    def readline(self):
        output = b''
        output = output.decode('utf-8')[:-3]
        output = output.split(sep=",")
        return output

    def is_on(self):
        return True


class RizeSimulation:
    def __init__(self, values):
        self.values = values
        self.num_values_emitted = 0

    def is_on(self):
        # Simulation is active while we have data
        return self.num_values_emitted < len(self.values)

    def readline(self):
        time.sleep(.001)
        if self.is_on():
            output = self.values[self.num_values_emitted]
            self.num_values_emitted = self.num_values_emitted + 1
            return output
