import time

import serial


class Magnetometer:
    def __init__(self, port='/dev/ttyACM0'):
        self.com = serial.Serial(port)
        self.first_readings = True

    def get_magnetic_field(self):
        data = self.com.readline()
        data = data[:-2].split(b" ")

        if self.first_readings:
            self.first_readings = False
            pass

        magnetic_field = [0, 0, 0]
        for i, byte in enumerate(data):
            magnetic_field[i] = float(byte)

        return magnetic_field
