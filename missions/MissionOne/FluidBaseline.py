import time

from pydispatch import dispatcher

from Pump import MockPump

import threading

class FluidBaseline:
    def __init__(self):
        self.current_state = [False, False, False]
        self.has_the_pump_been_on = False
        self.terminate_flag_one = False
        self.terminate_flag_two = False
        self.terminate_bool = False
        self.pump = MockPump()
        print("THE MOCK PUMP IS ON")
        dispatcher.connect(receiver=self.receive_current_state, signal="mission_1_state", sender="state_control")

    def receive_current_state(self, message):
        print('mission fluid baseline has received message: {}'.format(message))
        self.current_state = message

    def sensor_in_AIR_sensor_out_AIR(self):
        if (self.current_state[0] == True):
            return True
        else:
            return False

    def sensor_in_LIQUID_sensor_out_AIR(self):
        if (self.current_state[1] == True):
            return True
        else:
            return False

    def sensor_in_LIQUID_sensor_out_LIQUID(self):
        if (self.current_state[2] == True):
            return True
        else:
            return False

    def pump_tasks(self, state_system_object):
        bool_run_once = True
        bool_print_once = True
        bool_print_once_2 = True
        base_line_bool = True
        go = True
        while (go):
            if self.terminate_bool:
                print("We have terminated mission 1")
                state_system_object.set_state(2)
                go = False
            else:
                # Set Flag for initialization state where pump will start pumping without any input from the chip
                if (self.sensor_in_LIQUID_sensor_out_AIR()):
                    self.has_the_pump_been_on = True
                if not self.has_the_pump_been_on:
                    self.pump.pumping_with_delays(delay_on=3, delay_off=2, rate=0.075, direction="WDR")
                # State 1 Liquid at sensor in Air still at sensor out
                # chip needs to fill with liquid
                if (self.sensor_in_LIQUID_sensor_out_AIR()):
                    if not self.terminate_flag_one:
                        self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.065, direction="WDR")
                    elif (self.terminate_flag_one):
                        time.sleep(2)
                        if (base_line_bool):
                            print("sending over baseline")
                            state_system_object.set_baseline()
                            base_line_bool = False
                        self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="WDR")
                        if (bool_print_once):
                            print("I am now in state Liquid Air, and finalizing pumping")
                            bool_print_once = False
                        self.terminate_flag_two = True
                # State 2 Liquid on the chip
                # now push the liquid back a little bit and push the other way
                if (self.sensor_in_LIQUID_sensor_out_LIQUID()):
                    if not self.terminate_flag_two:
                        if (bool_run_once):
                            self.pump.pumping_with_delays(delay_on=3, delay_off=0, rate=0.4, direction="INF")
                            print("I just pushed back really hard")
                            bool_run_once = False
                        self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
                        self.terminate_flag_one = True
                    else:
                        print("I am in state liquid liquid and I'm about to terminate the program")
                        self.terminate_bool = True