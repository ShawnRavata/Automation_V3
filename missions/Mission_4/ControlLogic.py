from pydispatch import dispatcher
import time
from get_impedance_range import get_impedance_state
from NameList import NameList

class ControlLogic():
    def __init__(self):
        self.well_25 = ""
        self.well_27 = ""
        self.well_26 = ""
        self.well_24 = ""
        self.NameList = NameList()
        self.state = 0

    def control_state_logic(self, output):
        well_25 = get_impedance_state(output["IMPEDANCE 25"])
        well_27 = get_impedance_state(output["IMPEDANCE 27"])
        well_26 = get_impedance_state(output["IMPEDANCE 26"])
        well_24 = get_impedance_state(output["IMPEDANCE 24"])
        if (well_24 != well_25 != self.well_25 or well_27 != self.well_27 or well_26 != self.well_26):
            self.well_24 = well_24
            self.well_25 = well_25
            self.well_26 = well_26
            self.well_27 = well_27
            print("well 25:", well_25,
                  "well 24:", well_24,
                  "well 26:", well_26,
                  "well 27:", well_27,
                  "current time:", time.ctime())
            print("well 25 value:", output["IMPEDANCE 25"],
                  "well 25 value:", output["IMPEDANCE 25"],
                  "well 26 value:", output["IMPEDANCE 26"],
                  "well 27 value:", output["IMPEDANCE 27"]
                  )
            self.pumping_action(well_24=well_24, well_25=well_25, well_26=well_26, well_27=well_27,output=output)
            self.state_4_control_sends_current_state()

    def pumping_action(self, well_24, well_25, well_26, well_27, output):
        if (well_24 == "LIQUID" and well_25 == "AIR" and well_26 == "LIQUID" or well_27 == "LIQUID"):
            self.state = 1
        if (well_24 == "LIQUID" and well_25 == "LIQUID" and well_26 == "LIQUID" or well_27 == "LIQUID"):
            self.state = 2
        if (well_24 == "LIQUID" and well_25 == "LIQUID" and well_26 == "LIQUID" or well_27 == "AIR"):
            self.state = 3
        if (well_24 == "LIQUID" and well_25 == "LIQUID" and well_26 == "AIR" or well_27 == "AIR"):
            self.state = 4
        if (well_24 == "LIQUID" and well_25 == "AIR" and well_26 == "AIR" or well_27 == "AIR"):
            self.state = 5
        if (well_24 == "AIR" and well_25 == "AIR" and well_26 == "AIR" or well_27 == "AIR"):
            self.state = 6
    def state_4_control_sends_current_state(self):
        dispatcher.send(message=self.state, signal="state_4" , sender="state_control_4")