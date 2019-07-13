import time

import serial


class Pump():
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
            self.setup(rate=rate, direction=direction)
            time.sleep(.02)
            self.start()
            time.sleep(delay_on)
            delay_bool = True
        if delay_bool == True:
            time.sleep(.02)
            self.stop()
            time.sleep(delay_off)
            delay_bool = False

    def send_command(self, command):
        command += '\r\n'
        command = bytes(command, 'utf-8')
        self.pump_serial.write(command)

    def set_rate(self, rate):
        rate_command = "RAT " + str(rate) + "MM"
        self.send_command(rate_command)

    def set_direction(self, direction):
        direction_command = "DIR " + direction
        self.send_command(direction_command)

    def start(self):
        self.send_command("RUN")

    def stop(self):
        self.send_command("STP")

    def setup(self, rate, direction):
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
