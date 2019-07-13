import time
from pydispatch import dispatcher

class mission_1_control_logic():
    def __init__(self):
        self.one_hot_state_length = 3
        self.one_hot_state = []
        for i in range(self.one_hot_state_length):
            self.one_hot_state.append(False)
        print("initialized states:", self.one_hot_state)
        self.well_25 = ""
        self.well_27 = ""
        self.well_26 = ""
        self.is_on = False

    def mission_1_state(self ,output):
        well_25 = self.get_impedance_state(output["IMPEDANCE 25"])
        well_27 = self.get_impedance_state(output["IMPEDANCE 27"])
        well_26 = self.get_impedance_state(output["IMPEDANCE 26"])
        if (well_25 != self.well_25 or well_27 != self.well_27 or well_26 != self.well_26):
            self.well_25 = well_25
            self.well_27 = well_27
            self.well_26 = well_26
            self.pumping_action(well_25=well_25, well_27=well_27, well_26=well_26)
            print("well 25:", well_25, "well 27:", well_27, "well 26:", well_26,
                  "current time:", time.ctime())
            print("well 25 value:", output["IMPEDANCE 25"], "well 27 value:",
                  output["IMPEDANCE 27"], "well 26 value:", output["IMPEDANCE 26"])
            self.state_1_control_sends_current_state()

    def pumping_action(self, well_25, well_27, well_26):
        # start is air start pumping
        if (well_25 == "AIR" and well_27 == "AIR"):
            self.set_all_states_false()
            self.one_hot_state[0] = True
        if (well_25 == "LIQUID" and well_27 == "AIR"):
            self.set_all_states_false()
            self.one_hot_state[1] = True
        if (well_25 == "LIQUID" and well_27 == "LIQUID"):
            self.set_all_states_false()
            self.one_hot_state[2] = True

    def get_impedance_state(self, impedance):
        if impedance > 50_000:
            return "AIR"
        elif impedance > 7_500:
            return "RESIDUE"
        elif impedance > 1_000:
            return "LIQUID"
        else:
            return "ERROR"
    def state_1_control_sends_current_state(self):
        dispatcher.send(message=self.one_hot_state, signal="mission_1_state", sender="state_control")
    def set_all_states_false(self):
        for i in range(self.one_hot_state_length):
            self.one_hot_state[i] = False