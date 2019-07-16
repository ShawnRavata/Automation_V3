import time

import serial

pump_serial = serial.Serial(
            port='COM9',
            baudrate=19200,
            bytesize=8,
            stopbits=1,
            parity='N',
        )
class Pump():
    def __init__(self):
        pass

    def pumping_with_delays(self, delay_on, delay_off, rate, direction):
        delay_bool = False
        if delay_bool == False:
            self.setup(rate=rate, direction=direction)
            self.start()
            time.sleep(delay_on)
            delay_bool = True
        if delay_bool == True:
            self.stop()
            time.sleep(delay_off)
            delay_bool = False

    def send_command(self, command):
        command += '\r\n'
        command = bytes(command, 'utf-8')
        pump_serial.write(command)

    def set_rate(self, rate):
        rate_command = "RAT " + str(rate) + "MM"
        self.send_command(rate_command)

    def set_direction(self, direction):
        direction_command = "DIR " + direction
        self.send_command(direction_command)

    def start(self):
        time.sleep(.02)
        self.send_command("RUN")

    def stop(self):
        time.sleep(.02)
        self.send_command("STP")

    def setup(self, rate, direction):
        time.sleep(.02)
        self.set_rate(rate=rate)
        time.sleep(.02)
        self.set_direction(direction=direction)


class MockPump():
    def __init__(self):
        self.filename = "PumpLog.txt"

    def pumping_with_delays(self, delay_on, delay_off, rate, direction):
        with open(self.filename, 'a') as the_file:
            the_file.write(
                str(time.ctime()) + ", delay on:" + str(delay_on) + ", delay off:" + str(delay_off) + ", rate:"
                + str(rate) + ", direction:" + str(direction)+"\n")

    def send_command(self, command):
        pass

    def set_rate(self, rate):
        pass

    def set_direction(self, direction):
        pass

    def start(self):
        with open(self.filename, 'a') as the_file:
            the_file.write(str(time.ctime()) + ", START"+"\n")

    def stop(self):
        with open(self.filename, 'a') as the_file:
            the_file.write(str(time.ctime()) + ", STOP"+"\n")

    def setup(self, rate, direction):
        pass
