import time

import serial


class Magnetometer:
    def __init__(self, port='/dev/ttyACM1'):
        self.com = serial.Serial(port, baudrate=9600, timeout=2)
        self.first_readings = True
        self.last_magnetic_field = [0, 0, 0]

    def get_magnetic_field(self):
        a = self.com.write(b"\x00")

        data = self.com.readline()

        if data == b"":
            return self.last_magnetic_field

        data = data[:-2].split(b" ")

        magnetic_field = [0, 0, 0]
        for i, byte in enumerate(data):
            magnetic_field[i] = float(byte)
        self.last_magnetic_field = magnetic_field
        return self.last_magnetic_field
