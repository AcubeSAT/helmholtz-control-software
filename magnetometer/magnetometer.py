import serial, time

class Magnetometer:

    def __init__(self, port='/dev/ttyUSB0'):
        self.serial_communication = serial.Serial(self.port)
        time.sleep(2)
    
    def get_magnetic_field(self):

