import serial

class PSU:
    # RIGOL DP712

    def __init__(self, port='/dev/ttyUSB0', channel='CH1'):
        self.max_current = 3
        self.max_voltage = 50
        self.channel = channel

        self.port = port
        self.serial_communication = serial.Serial(self.port)


    def set_voltage_and_current(self, voltage, current):
        command = (':APPLy '+self.channel+','+str(voltage)+','+str(current)+'\n').encode("utf-8")
        self.serial_communication.write(command)

    def set_voltage(self, voltage):
        command = (':APPLy '+str(voltage)+'\n').encode("utf-8")
        self.serial_communication.write(command)

    def set_current(self, current):
        command = (':APPLy ,' + str(current) + '\n').encode("utf-8")
        self.serial_communication.write(command)

    def get_requested_voltage(self, voltage, current):
        command = ':VOLT?\n'.encode("utf-8")
        self.serial_communication.write(command)
        voltage = (self.serial_communication.readline()).decode("utf-8")
        return voltage

    def get_requested_current(self, voltage):
        command = ':CURR?\n'.encode("utf-8")
        self.serial_communication.write(command)
        current = (self.serial_communication.readline()).decode("utf-8")
        return current

    def measure_voltage(self):
        command = (':MEAS:VOLT? '+serial.channel+'\n').encode("utf-8")
        self.serial_communication.write(command)
        voltage = (self.serial_communication.readline()).decode("utf-8")
        return voltage

    def measure_current(self):
        command = (':MEAS:CURR? '+serial.channel+'\n').encode("utf-8")
        self.serial_communication.write(command)
        current = (self.serial_communication.readline()).decode("utf-8")
        return current