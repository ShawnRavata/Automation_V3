from time import sleep

import pandas as pd
import serial

from NameList import NameList


class Rize:
    def __init__(self):
        self.subs = []
        self.arduino = serial.Serial(port="COM12", baudrate=115200)
        print("Arduino is connected", self.arduino.is_open)
        self.name_list_class_obj = NameList()
        self.name_list = NameList.get_name_string()

    def read_line(self):
        output = self.arduino.readline()
        output = output.decode('utf-8')[:-3].split(sep=",")
        if len(self.name_list) == len(output):
            return {key: float(val) for key, val in zip(self.name_list, output)}
        else:
            raise ValueError

    def is_on(self):
        return self.arduino.is_open


class RizeSimulation:
    def __init__(self):
        self.data = pd.read_csv("./data/embryo_in_automation_simulation.csv")
        self.data = self.data.to_dict('records')
        self.num_values_emitted = 0

    def is_on(self):
        # Simulation is active while we have data
        return self.num_values_emitted < len(self.data)

    def read_line(self):
        output = self.data[self.num_values_emitted]
        sleep(.01)
        self.num_values_emitted += 1
        return output
