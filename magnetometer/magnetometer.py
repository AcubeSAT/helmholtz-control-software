import time

import serial
import numpy as np

class Magnetometer:
    def __init__(self, port='/dev/ttyACM1'):
        self.com = serial.Serial(port, baudrate=9600, timeout=2)
        self.first_readings = True
        self.last_magnetic_field = [0, 0, 0]
        self.V = [-12.6343, 18.1653, -7.3313]
        self.W = [[1.0017, -0.1847, 0.2167],
                  [-0.1240, -1.0088, -0.2867],
                  [-0.2709, -0.2597, 1.0310]]

    def get_magnetic_field(self):
        while True:
            self.com.write(b"\x00")
            data = self.com.readline()
            # print(f"data is {data}")
            if data == b"" or data == b"0":
                continue
            
            #TODO: try to empty the serial buffer with a better way
            # Read all available data to prevent buffer overflow
            while self.com.in_waiting:
                _ = self.com.readline()

            # print(f"data is {data}")
            data = data[:-2].split(b" ")

            magnetic_field = [0, 0, 0]
            for i, byte in enumerate(data):
                try:
                    # print(f"byte is {byte}")
                    magnetic_field[i] = float(byte)
                except:
                    # If conversion fails, handle the error and retry
                    print(f"Error: Unable to convert byte to float. {byte}")
                    # print(f"magnetic field is {magnetic_field[i]}")
                    break
            else:
                # If all conversions were successful, update and return the magnetic field
                self.last_magnetic_field = np.subtract(magnetic_field, self.V)
                return self.last_magnetic_field
