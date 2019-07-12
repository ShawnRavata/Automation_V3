from arduino_publish_value import arduino_publish_value
import threading
from logger_controller import logger_controller
from state_system import state_system
from mission_1_fluid_baseline import mission_1_test

# creates the publishing class that will take in serial arduino output and the publish it to subscribers
rize = arduino_publish_value()

# register the csv logger to take published arduino data
logger_controller = logger_controller()
rize.register_subscriber(logger_controller.consume)

# register the state system subscriber
state_system_object = state_system()
rize.register_subscriber(state_system_object.consume)
t1 = threading.Thread(mission_1_test.state_change)

#while the arduino is connected keep publishing values
while(rize.is_on()):
    rize.process_value()