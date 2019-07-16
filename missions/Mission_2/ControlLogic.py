import time

from pydispatch import dispatcher

from NameList import NameList
from get_impedance_range import get_impedance_state


class ControlLogic():
    def __init__(self):
        self.well_25 = ""
        self.well_27 = ""
        self.well_26 = ""
        self.well_24 = ""
        self.embryo_log = {}
        self.embryo_event_list = []
        self.embryo_count = 0
        self.NameList = NameList()
        self.Sim = True
        self.state = 0
        self.baseline_impedance = {}
        self.state_1_flag = True
        self.run_once_1 = True
        if self.Sim != True:
            self.embryo_count = input("enter embryo count")

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
            self.pumping_action(well_24=well_24, well_25=well_25, well_26=well_26, well_27=well_27, output=output)
            self.state_2_control_sends_current_state()

    def pumping_action(self, well_24, well_25, well_26, well_27, output):
        if (well_25 == "LIQUID" and well_26 == "LIQUID" and (well_27 == "AIR" or well_27 == "RESIDUE")):
            self.state = 1
            if self.run_once_1 == True:
                self.set_baseline(output)
                self.run_once_1 = False
                print("set the baseline")
        elif (well_25 == "LIQUID" and well_26 == "LIQUID" and well_27 == "LIQUID"):
            self.state = 2
        elif ((well_25 == "AIR" or well_25 == "RESIDUE") and well_24 == "LIQUID"
              and well_26 == "LIQUID" and well_27 == "LIQUID"):
            self.state = 3
            if not self.check_for_embryo(output=output):
                print("WE ARE IN SIMULATION NO EMBRYOS MOVING TO NEXT MISSION")
                self.state = 4
        elif (self.state == 4):
            pass

    def state_2_control_sends_current_state(self):
        dispatcher.send(message=self.state, signal="state_2", sender="state_control_2")

    def set_baseline(self, baseline):
        impedance_list = self.NameList.get_impedance_list()
        new_baseline = {}
        for i in range(len(impedance_list)):
            new_baseline.update({impedance_list[i]: baseline[impedance_list[i]]})
        self.base_line_impedance = new_baseline

    def look_at_current_well_1_to_21(self, output):
        impedance_list = self.NameList.get_impedance_list()
        new_output = {}
        for i in range(len(impedance_list)):
            new_output.update({impedance_list[i]: output[impedance_list[i]]})
        return new_output

    def check_for_embryo(self, output):
        impedance_list = self.NameList.get_impedance_list()
        impedance_output = self.look_at_current_well_1_to_21(output)
        for i in range(len(impedance_list)):
            if impedance_output[impedance_list[i]] - self.base_line_impedance[impedance_list[i]] > 150:
                self.embryo_count += 1
                self.embryo_event_list.append("embryo event at well " + str(i))
                self.embryo_log.update({"well " + str(i): impedance_output[impedance_list[i]]})
        if self.embryo_count == 0:
            return False
        else:
            return True
