from SIMULATION_rize import RizeSimulation
import threading
from logger_controller import logger_controller
from state_system import state_system
from TEST_mission_1_fluid_baseline import mission_1_test
import time

# creates the publishing class that will take in serial arduino output and the publish it to subscribers
rize = RizeSimulation()

# register the csv logger to take published arduino data
logger_controller = logger_controller()
rize.register_subscriber(logger_controller.consume)

# register the state system subscriber
state_system_object = state_system()
rize.register_subscriber(state_system_object.consume)
print("Task main thread assigned to thread: {}".format(threading.current_thread().name))
#set up the state change thread
mission_1_object = mission_1_test(state_system_object)
t1 = threading.Thread(target=mission_1_object.state_change, args=[state_system_object.q])
t1.daemon=True
t1.start()


#while the arduino is connected keep publishing values
print("rize is on=", rize.is_on())
while(rize.is_on()):
    output=rize.readline()