from arduino_publish_value import arduino_publish_value
import threading
from logger_controller import logger_controller

# creates the publishing class that will take in serial arduino output and the publish it to subscribers
rize = arduino_publish_value()

# register the csv logger to take published arduino data
logger_controller = logger_controller()
rize.register_subscriber(logger_controller.consume)

#while the arduino is connected keep publishing values
while(rize.is_on()):
    rize.process_value()