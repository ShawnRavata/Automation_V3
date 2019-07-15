import time

from pydispatch import dispatcher
from get_impedance_range import get_impedance_state

class ControlLogic:
    def __init__(self):
        self.one_hot_state_length = 4
        self.one_hot_state = []
        for i in range(self.one_hot_state_length):
            self.one_hot_state.append(False)
        print("initialized states:", self.one_hot_state)
        self.well_25 = ""
        self.well_27 = ""
        self.well_26 = ""
        self.is_on = False
        self.flag_one = False

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
        if (well_25 == "AIR" and well_27 == "AIR"):
            self.set_all_states_false()
            self.one_hot_state[0] = True
        elif (well_25 == "LIQUID" and well_27 == "AIR"):
            self.set_all_states_false()
            self.one_hot_state[1] = True
        elif (well_25 == "LIQUID" and well_26 == "LIQUID" and well_27 == "LIQUID"):
            self.set_all_states_false()
            self.one_hot_state[2] = True
            self.flag_one = True
            print("we set the flag to true")
        elif (well_25 == "LIQUID" and well_26 == "LIQUID" and
                well_27 == "AIR" and self.flag_one == True):
            print("Im here")
            self.set_all_states_false()
            self.one_hot_state[3] = True

    def state_1_control_sends_current_state(self):
        dispatcher.send(message=self.one_hot_state, signal="mission_1_state", sender="state_control")

    def set_all_states_false(self):
        for i in range(self.one_hot_state_length):
            self.one_hot_state[i] = False
