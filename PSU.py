import pyvisa
import time

class PSU:
    """
    Power supply unit control software for Spacedot's Helmholtz cage.
    """

    def __init__(self, channel='CH1', model='DP712'):
        self.max_current = 3
        self.max_voltage = 50

        assert model in ['DP712', 'SPD3303C']

        connected_devices = pyvisa.ResourceManager().list_resources()
        if len(connected_devices) > 1:
            if model == 'DP712':
                psu = 'ASRL/dev/ttyUSB0::INSTR'
            else:
                psu = 'USB0::1155::30016::SPD3EEEC6R0509::0::INSTR'
        else:
            psu = 'ASRL/dev/ttyUSB0::INSTR'

        self.channel = channel
        self.model = model
        self.device = pyvisa.ResourceManager().open_resource(psu)

    def set_voltage_and_current(self, voltage, current):
        assert voltage <= self.max_voltage
        assert current <= self.max_current

        command = (':APPLy ' + self.channel + ',' + str(voltage) + ',' + str(current))
        self.device.write(command)

    def set_voltage(self, voltage):
        assert voltage <= self.max_voltage
        if self.model == "DP712":
            command = (':VOLT ' + str(voltage))
        else:
            command = (self.channel + ':VOLT ' + str(voltage))
        self.device.write(command)

    def set_current(self, current):
        assert current <= self.max_current
        if self.model == "DP712":
            command = (':CURR ' + str(current))
        else:
            command = (self.channel + ':CURR ' + str(current))
        self.device.write(command)

    def get_current(self):
        command = ':CURR?'

        self.device.write(command)
        return self.device.query(command, delay=0.01)

    def get_voltage(self):
        command = ':VOLT?'

        self.device.write(command)
        return self.device.query(command, delay=0.01)

    def measure_current(self):
        command = ':MEAS:CURR?'

        self.device.write(command)
        time.sleep(0.5)
        return self.device.query(command, delay=0.01)

    def measure_voltage(self):
        command = ':MEAS:VOLT?'

        self.device.write(command)
        time.sleep(0.5)
        return self.device.query(command, delay=0.01)

    def set_channel(self, channel):
        self.channel = channel
