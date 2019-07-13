import threading

from LoggerController import LoggerController
from Rize import RizeSimulation, Rize
from StateSystem import StateSystem
from missions.MissionOne.FluidBaselineMock import FluidBaselineMock

# creates the publishing class that will take in serial arduino output and the publish it to subscribers
is_simulation = True
if is_simulation:
    rize = RizeSimulation()
else:
    rize = Rize()

# register the csv logger to take published arduino data
logger_controller = LoggerController()
rize.register_subscriber(logger_controller.consume)

# register the state system subscriber
state_system_object = StateSystem()
rize.register_subscriber(state_system_object.consume)
print("Task main thread assigned to thread: {}".format(threading.current_thread().name))
# set up the state change thread
mission_1_object = FluidBaselineMock(state_system_object)
t1 = threading.Thread(target=mission_1_object.state_change, args=[state_system_object.q])
t1.daemon = True
t1.start()

# while the arduino is connected keep publishing values
print("rize is on=", rize.is_on())
while rize.is_on():
    output = rize.process_value()
