import time
import serial
import pyvisa


class PSU:
    """
    Power supply unit control software for Spacedot's Helmholtz cage.
    """

    def __init__(self, channel='CH1', model='DP712'):
        self.max_current = 3
        self.max_voltage = 50

        assert model in ['DP712', 'SPD3303C']

        connected_devices = pyvisa.ResourceManager().list_resources()
        if len(connected_devices) == 2:
            if model == 'DP712':
                psu = connected_devices[0]
            else:
                psu = connected_devices[1]
        else:
            psu = connected_devices[0]

        self.channel = channel

        self.device = pyvisa.ResourceManager().open_resource(psu)

    def set_voltage_and_current(self, voltage, current):
        assert voltage <= self.max_voltage
        assert current <= self.max_current

        command = (self.channel + ',' + str(voltage) + ',' + str(current))
        self.device.write(command)

    def set_voltage(self, voltage):
        assert voltage <= self.max_voltage
        command = (self.channel + ':VOLT ' + str(voltage))
        self.device.write(command)

    def set_current(self, current):
        assert current <= self.max_current

        command = (self.channel + ':CURR ' + str(current))
        self.device.write(command)

    def get_current(self):
        command = ':CURR?'

        self.visa_device.write(command)
        return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def get_voltage(self):
        command = ':VOLT?'

        self.visa_device.write(command)
        return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def measure_current(self):
        """
        Measures the current flowing out of the PSU.
        Returns: the measured current

        """
        command = ':MEAS:CURR?'

        self.device.write(command)
        return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def measure_voltage(self):
        """
        Measures the voltage at the ends of the PSU.
        Returns: the measured voltage

        """
        command = ':MEAS:VOLT?'

        self.device.write(command)
        return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def set_channel(self, channel):
        self.channel = channel
