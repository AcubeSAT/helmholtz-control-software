import time
import serial
import pyvisa


class PSU:
    """
    Power supply unit control software for Spacedot's Helmholtz cage.
    """

    def __init__(self, port='/dev/ttyUSB0', channel='CH1', model='DP712'):
        self.max_current = 3
        self.max_voltage = 50

        assert model in ['DP712', 'SPD3303C']

        self.model = model

        if self.model == 'DP712':
            assert channel == 'CH1'
            self.channel = channel
            self.port = port
            try:
                self.serial_communication = serial.Serial(self.port)
            except:
                raise Exception("Device not found")

        else:
            assert channel in ['CH1', 'CH2']
            self.channel = channel
            device = pyvisa.ResourceManager().list_resources()
            self.visa_device = ups = pyvisa.ResourceManager().open_resource(device[0])

    def set_voltage_and_current(self, voltage, current):
        """
        Sets voltage and current of the DP712 power supply unit.
        Args:
            voltage: the desired voltage
            current: the desired current
        """
        assert self.model == "DP712"
        assert voltage <= self.max_voltage
        assert current <= self.max_current

        command = (':APPLy ' + self.channel + ',' + str(voltage) + ',' + str(current) + '\n').encode("utf-8")
        self.serial_communication.write(command)

    def set_voltage(self, voltage):
        """
        Desired voltage setter.
        Args:
            voltage: the desired voltage
        """
        assert voltage <= self.max_voltage
        if self.model == 'DP712':
            command = (':APPLy ' + str(voltage) + '\n').encode("utf-8")
            self.serial_communication.write(command)
        else:
            command = (self.channel + ':VOLT ' + str(voltage) + '\n')
            self.visa_device.write(command)

    def set_current(self, current):
        """
        Desired current setter.
        Args:
            current: the desire current
        """
        assert current <= self.max_current
        if self.model == 'DP712':
            command = (':APPLy ,' + str(current) + '\n').encode("utf-8")
            self.serial_communication.write(command)
        else:
            command = (self.channel + ':CURR ' + str(current))
            self.visa_device.write(command)

    def get_requested_quantity(self, request_command):
        """
        Request the current voltage or current of the PSU.
        Args:
            request_command: the command for voltage or current

        Returns:
            The value of the requested quantity
        """
        assert request_command in ['voltage', 'current']

        if request_command == 'voltage':
            command = ':VOLT?\n'.encode('utf-8')
        else:
            command = ':CURR?\n'.encode('utf-8')

        if self.model == 'DP712':
            self.serial_communication.write(command)
            return (self.serial_communication.readline()).decode("utf-8")
        else:
            self.visa_device.write(command.decode('utf-8'))
            return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def measure_value(self, request_command):
        """
        Measures the current voltage or current of the PSU.
        Args:
            request_command: the command for voltage or current

        Returns:
            The measured PSU value
        """
        assert request_command in ['voltage', 'current']
        if request_command == 'voltage':
            command = ':MEAS:VOLT?'.encode('utf-8')
        else:
            command = ':MEAS:CURR?'.encode('utf-8')

        if self.model == 'DP712':
            self.serial_communication.write(command)
            return (self.serial_communication.readline()).decode("utf-8")
        else:
            self.visa_device.write(command.decode('utf-8'))
            return self.visa_device.query(command.decode('utf-8'), delay=0.01)

    def set_channel(self, channel):
        """
        Changes the channel of the PSU.
        Args:
            channel: the desired new channel
        """
        self.channel = channel
