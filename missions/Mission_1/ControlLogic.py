import time

from pydispatch import dispatcher
from get_impedance_range import get_impedance_state

class ControlLogic:
    def __init__(self):
        self.one_hot_state = 0
        print("initialized states:", self.one_hot_state)
        self.well_25 = ""
        self.well_27 = ""
        self.well_26 = ""
        self.is_on = False
        self.flag_one = False
        # testing print statements
        self.print_once_1 = True
        self.print_once_2 = True
        self.print_once_3 = True
        self.print_once_4 = True

    def mission_1_state(self, output):
        well_25 = get_impedance_state(output["IMPEDANCE 25"])
        well_27 = get_impedance_state(output["IMPEDANCE 27"])
        well_26 = get_impedance_state(output["IMPEDANCE 26"])
        if (well_25 != self.well_25 or well_27 != self.well_27 or well_26 != self.well_26):
            self.well_25 = well_25
            self.well_27 = well_27
            self.well_26 = well_26
            print("well 25:", well_25, "well 26:", well_26, "well 27:", well_27,
                  "current time:", time.ctime())
            print("well 25 value:", output["IMPEDANCE 25"], "well 26 value:", output["IMPEDANCE 26"]
                  , "well 27 value:", output["IMPEDANCE 27"]
                  )
            self.pumping_action(well_25=well_25, well_27=well_27, well_26=well_26)
            self.state_1_control_sends_current_state()


    def pumping_action(self, well_25, well_27, well_26):
        # start is air start pumping
        if ((well_25 == "AIR" or well_25 == "RESIDUE") and well_27 == "AIR"):
            if (self.print_once_1):
                print("Fluid baseline state[0]")
                self.print_once_1 = False
            self.one_hot_state = 0
        elif (well_25 == "LIQUID" and well_27 == "AIR"):
            if (self.print_once_2):
                print("Fluid baseline state[1]")
                self.print_once_2 = False
            self.one_hot_state = 1
        elif (well_25 == "LIQUID" and well_26 == "LIQUID" and well_27 == "LIQUID"):
            if (self.print_once_3):
                print("Fluid baseline state[2]")
                self.print_once_3 = False
            self.one_hot_state = 2
            self.flag_one = True
            print("we set the flag to true")
        elif (well_25 == "LIQUID" and well_26 == "LIQUID" and
                well_27 == "AIR" and self.flag_one == True):
            if (self.print_once_4):
                print("Fluid baseline state[3]")
                self.print_once_4 = False
            self.one_hot_state = 3

    def state_1_control_sends_current_state(self):
        dispatcher.send(message=self.one_hot_state, signal="mission_1_state", sender="state_control")


