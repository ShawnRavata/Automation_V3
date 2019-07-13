import time
import pandas as pd
from name_list import name_list

class Rize:
    def readline(self):
        output = b''
        output = output.decode('utf-8')[:-3]
        output = output.split(sep=",")
        return output

    def is_on(self):
        return True



class RizeSimulation:
    def __init__(self):
        self.data = pd.read_csv("embryo_in_automation_simulation.csv")
        self.data = self.data.to_dict('records')
        self.values = self.data
        self.num_values_emitted = 0
        self.subs = []

    def is_on(self):
        # Simulation is active while we have data
        return self.num_values_emitted < len(self.values)

    def readline(self):
        time.sleep(.5)
        if self.is_on():
            output = self.values[self.num_values_emitted]
            self.num_values_emitted = self.num_values_emitted + 1
            self.__publish(output=output)

    def register_subscriber(self, sub):
        self.subs += [sub]

    def __publish(self, output):
        # Calls each of the subscribers with the output from the rize
        for sub in self.subs:
            sub(output)
