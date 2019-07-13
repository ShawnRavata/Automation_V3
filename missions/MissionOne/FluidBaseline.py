import threading
import time

from pydispatch import dispatcher
from signals_list_s import signals_list


class FluidBaseline:
    def __init__(self, serial):
        self.current_state = [False, False, False]
        self.serial = serial
        self.signal = signals_list()
        self.has_the_pump_been_on = False
        self.delay = False
        self.terminate_flag_one = False
        self.terminate_flag_two = False
        self.terminate_bool = False
        self.event = threading.Event()
        self.state_1 = True
        self.state_2 = False
        dispatcher.connect(receiver=self.receive_current_state, signal="mission_1_state", sender="state_control")

        dispatcher.connect(receiver=self.state_1_receiver, signal="mission 1 terminate", sender="mission 1")
        dispatcher.connect(receiver=self.state_2_receiver, signal="mission 2 start", sender="mission 1")

    def state_1_receiver(self, message):
        self.state_1 = message
        print("state 1 is received as {}".format(message))
        print(self.state_1)

    def state_2_receiver(self, message):
        self.state_2 = message
        print("state 2 is received as {}".format(message))
        print(self.state_2)

    def receive_current_state(self, message):
        print('mission fluid baseline has received message: {}'.format(message))
        self.current_state = message

    def receive_event(self, message):
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

    def state_control(self, main_object):
        print("Task 1 thread assigned to thread: {}".format(threading.current_thread().name))
        bool_run_once = True
        bool_print_once = True
        bool_print_once_2 = True
        base_line_bool = True
        # testing self terminate
        # self.terminate_bool = True
        # self.event.set()
        while (True):
            # self.event.wait()
            if self.terminate_bool:
                # time.sleep(0.2)
                # self.pump_stop()
                if (bool_print_once_2 == True):
                    print("We have terminated mission 1")
                    bool_print_once_2 = False
                    print(main_object.state_2)
                    main_object.state_2 = True
                    main_object.state_1 = False
                    print("printing at the end of terminate: main obj state 2 status:", main_object.state_2)

                # self.event.clear()
            else:
                # Set Flag for initialization state where pump will start pumping without any input from the chip
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if (self.sensor_in_LIQUID_sensor_out_AIR()):
                    self.has_the_pump_been_on = True
                if not self.has_the_pump_been_on:
                    time.sleep(.02)
                    self.pump_set_rate(rate=0.075)
                    time.sleep(.02)
                    self.pumping_with_delays(delay_on=3, delay_off=2, rate=0.075, direction="WDR")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # State 1 Liquid at sensor in Air still at sensor out
                # chip needs to fill with liquid
                if (self.sensor_in_LIQUID_sensor_out_AIR()):
                    if not self.terminate_flag_one:
                        self.pumping_with_delays(delay_on=2, delay_off=3, rate=0.065, direction="WDR")
                    elif (self.terminate_flag_one):
                        time.sleep(2)
                        if (base_line_bool):
                            dispatcher.send(message=base_line_bool, signal="base line", sender="mission 1")
                            print("sending over baseline")
                            base_line_bool = False
                        self.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="WDR")
                        if (bool_print_once):
                            print("I am now in state Liquid Air, and finalizing pumping")
                            bool_print_once = False
                        self.terminate_flag_two = True
                # State 2 Liquid on the chip
                # now push the liquid back a little bit and push the other way
                if (self.sensor_in_LIQUID_sensor_out_LIQUID()):
                    if not self.terminate_flag_two:
                        if (bool_run_once):
                            self.pumping_with_delays(delay_on=3, delay_off=0, rate=0.4, direction="INF")
                            print("I just pushed back really hard")
                            bool_run_once = False
                        self.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
                        self.terminate_flag_one = True
                    else:
                        print("I am in state liquid liquid and I'm about to terminate the program")
                        self.terminate_bool = True

    def pumping_with_delays(self, delay_on, delay_off, rate, direction):
        delay_bool = False
        if delay_bool == False:
            time.sleep(.02)
            self.pump_setup(rate=rate, direction=direction)
            time.sleep(.02)
            self.pump_start()
            time.sleep(delay_on)
            delay_bool = True
        if delay_bool == True:
            time.sleep(.02)
            self.pump_stop()
            time.sleep(delay_off)
            delay_bool = False

    def sendPumpCommand(self, command):
        command += '\r\n'
        command = bytes(command, 'utf-8')
        self.serial.write(command)

    def pump_set_rate(self, rate):
        rate_command = "RAT " + str(rate) + "MM"
        self.sendPumpCommand(rate_command)

    def pump_set_direction(self, direction):
        direction_command = "DIR " + direction
        self.sendPumpCommand(direction_command)

    def pump_start(self):
        self.sendPumpCommand("RUN")

    def pump_stop(self):
        self.sendPumpCommand("STP")

    def pump_setup(self, rate, direction):
        self.pump_set_rate(rate=rate)
        time.sleep(.02)
        self.pump_set_direction(direction=direction)

    def set_up(self):
        input("Press Enter to continue...")
        self.pump_setup(rate=.05, direction="WDR")
