import time
import serial
class pump_commands():
    def __init__(self):
        self.pump_serial = serial.Serial(
            port='COM10',
            baudrate=19200,
            bytesize=8,
            stopbits=1,
            parity='N',
        )

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
        self.pump_serial.write(command)

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
