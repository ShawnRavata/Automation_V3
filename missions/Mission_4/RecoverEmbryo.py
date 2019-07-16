from pydispatch import dispatcher
from Pump import Pump

class Recover():
    def __init__(self):
        self.current_state = 0
        self.pump = Pump()
        dispatcher.connect(receiver=self.receive_current_state, signal="mission_2_state", sender="state_control_2")

    def receive_current_state(self, message):
        print('mission recover has received message: {}'.format(message))
        self.current_state = message

    def pump_tasks(self,state_system):
        go = True
        while(go):
            if(self.current_state == 1):
                self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
            elif(self.current_state == 2):
                self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
            elif (self.current_state == 3):
                self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
            elif (self.current_state == 4):
                self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
            elif (self.current_state == 5):
                self.pump.pumping_with_delays(delay_on=2, delay_off=3, rate=0.035, direction="INF")
            elif (self.current_state == 6):
                self.pump.stop()