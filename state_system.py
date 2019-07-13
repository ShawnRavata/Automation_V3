from queue import Queue
from TEST_mission_1_fluid_baseline import mission_1_test
import threading

class state_system():
    def __init__(self):
        self.output = {}
        self.state = 1
        self.q = Queue()
        self.q.put(self.state)
        self.base_line = {}


    def consume(self, output):
        self.output = output
        if(self.state == 1):
            print("I am here in mission 1")
        if(self.state == 2):
            print("Im here in mission 2")
        if(self.state == 3):
            print("Im here in mission 3")
        if(self.state == 4):
            print("I'm here in mission 4")

    def q_set(self, q):
        self.state = q




