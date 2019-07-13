import time

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

    def register_subscriber(self, sub):
        self.subs += [sub]

    def process_value(self):
        output = self.arduino.readline()
        try:
            output = output.decode('utf-8')[:-3].split(sep=",")
            # I have an error where some values get cut off from the arduino and this is the dirty fix to solve it
            if len(self.name_list) == len(output):
                output = {key: float(val) for key, val in zip(self.name_list, output)}
                self.__publish(output)
            # else:
            # print("****Arduino Value Send Error*****")
            # print(output)
            # print("^^^^Arduino Value Send Error^^^^")
        except TypeError:
            pass
            # print("TYPE ERROR DANIEL")
        except UnicodeDecodeError:
            pass
            # print("UNICODE DECODE ERROR DANIEL")
        except ValueError:
            pass
            # print("VALUE ERROR DANIEL")

    def is_on(self):
        return self.arduino.is_open

    def __publish(self, output):
        # Calls each of the subscribers with the output from the rize
        for sub in self.subs:
            sub(output)


class RizeSimulation:
    def __init__(self):
        self.data = pd.read_csv("./data/embryo_in_automation_simulation.csv")
        self.data = self.data.to_dict('records')
        self.values = self.data
        self.num_values_emitted = 0
        self.subs = []

    def is_on(self):
        # Simulation is active while we have data
        return self.num_values_emitted < len(self.values)

    def process_value(self):
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
