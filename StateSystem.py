from missions.Mission_1.ControlLogic import ControlLogic as Control_1
from missions.Mission_2.ControlLogic import ControlLogic as Control_2
from NameList import NameList

class StateSystem:
    def __init__(self):
        self.output = {}
        self.state = 1
        self.base_line_impedance = {}
        self.control_1_obj = Control_1()
        self.control_2_obj = Control_2()
        self.print_once_1 = True
        self.NameList = NameList()

    def consume(self, output):
        self.output = output
        if self.state == 1:
            # receives the signal from mission 1 to set the baseline
            # calls the math control logic for mission 1
            self.control_1_obj.mission_1_state(output=self.output)
        if self.state == 2:
            if self.print_once_1:
                print("Im here in mission 2")
                self.print_once_1 = False
            self.control_2_obj.control_state_logic(output=output)
        if self.state == 3:
            print("Im here in mission 3")
        if self.state == 4:
            print("I'm here in mission 4")

    def set_state(self, state):
        self.state = state

