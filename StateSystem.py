from missions.Mission_1.ControlLogic import ControlLogic as Control_1


class StateSystem:
    def __init__(self):
        self.output = {}
        self.state = 1
        self.base_line = {}
        self.base_line_set = False
        self.control_1_obj = Control_1()
        self.print_once_1 = True

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
        if self.state == 3:
            print("Im here in mission 3")
        if self.state == 4:
            print("I'm here in mission 4")

    def set_state(self, state):
        self.state = state

    def set_baseline(self):
        print("your fluid baseline value is set")
        self.base_line = self.output
