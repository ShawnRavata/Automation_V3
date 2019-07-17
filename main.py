import threading
import multiprocessing

from LoggerController import LoggerController
from Rize import RizeSimulation, Rize, read_line
from StateSystem import StateSystem
from missions.Mission_1.FluidBaseline import FluidBaseline
from missions.Mission_2.EmbryoIn import EmbryoIn

class output():
    def __init__(self):
        self.output = {}
    def get_output(self,output):
        self.output = output
    def return_output(self):
        return self.output

output_object = output()
# creates the publishing class that will take in serial arduino output and the publish it to subscribers
is_simulation = False

if is_simulation:
    rize = RizeSimulation()
else:
    rize = Rize()
    read_object = read_line(rize=rize)
    m1 = multiprocessing.Process(target=read_object.read_the_line)
    m1.start()
# register the csv logger to take published arduino data
logger_controller = LoggerController()
rize.register_subscriber(logger_controller.consume)

# register the state system subscriber
state_system_object = StateSystem()
rize.register_subscriber(state_system_object.consume)
print("Task main thread assigned to thread: {}".format(threading.current_thread().name))
# set up the state change thread
mission_2_object = EmbryoIn()
mission_1_object = FluidBaseline()
t1 = threading.Thread(target=mission_1_object.pump_tasks, args=(state_system_object,))
t1.daemon = True
t1.start()
t2 = threading.Thread(target=mission_2_object.pump_tasks, args=[state_system_object])
t2.daemon = True
t2.start()
while True:
    pass
