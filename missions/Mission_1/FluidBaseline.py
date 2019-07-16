
from pydispatch import dispatcher

from Pump import Pump

class FluidBaseline:
    def __init__(self):
        self.current_state = 0
        self.has_the_pump_been_on = False
        self.terminate_flag_one = False
        self.terminate_flag_two = False
        self.terminate_bool = False
        self.pump = Pump()
        dispatcher.connect(receiver=self.receive_current_state, signal="mission_1_state", sender="state_control")
        self.bool_run_once = True
        self.bool_run_once_1 = True
        self.bool_run_once_2 = True
        self.base_line_bool = True
        self.go = True
        # testing prints
        self.print_once_1 = True
        self.print_once_2 = True
        self.print_once_3 = True
        self.print_once_4 = True
    def receive_current_state(self, message):
        print('mission fluid baseline has received message: {}'.format(message))
        self.current_state = message

    def sensor_in_AIR_sensor_out_AIR(self):
        if (self.current_state[0] == True):
            return True
        else:
            return False


    def pump_tasks(self, state_system_object):
        while (self.go):
            if self.terminate_bool:
                print("We have terminated mission 1")
                state_system_object.set_state(2)
                self.go = False
            else:
                # Set Flag for initialization state where pump will start pumping without any input from the chip
                if self.current_state == 0:
                    self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.070, direction="WDR")
                if (self.current_state == 1):
                    self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.050, direction="WDR")
                # State 2 Liquid on the chip
                # now push the liquid back a little bit and push the other way
                if (self.current_state == 2):
                    self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
                if(self.current_state == 3):
                    self.pump.stop()
                    if (self.base_line_bool):
                        print("sending over baseline")
                        state_system_object.set_baseline()
                        self.base_line_bool = False
                        self.terminate_bool = True