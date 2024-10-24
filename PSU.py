import pyvisa
import time

class PSU:
    """
    Power supply unit control software for Spacedot's Helmholtz cage.
    """

    def __init__(self, channel='CH1', model='DP712'):
        self.max_current = 3
        self.max_voltage = 30

        assert model in ['DP712', 'SPD3303C']

        connected_devices = pyvisa.ResourceManager().list_resources()
        # print(f"Connected devices are: {connected_devices}")
        # print(f"length is: {len(connected_devices)}")
        if len(connected_devices) > 0:
            if model == 'DP712':
                psu = 'ASRL/dev/ttyUSB0::INSTR'
            else:
                psu = 'USB0::1155::30016::SPD3EEEC6R0509::0::INSTR'
        else:
            print("There are not connected devices")

        self.channel = channel
        self.model = model
        self.device = pyvisa.ResourceManager().open_resource(psu)
        print(f"PSU {self.model} connected succesfully")

    def set_overcurrent_protection(self):
        if self.model == 'DP712':
            command = ':OUTP:OCP:CLEAR'
            self.device.write(command)
            time.sleep(0.1)
            command = ':OUTP:OCP ON'
            self.device.write(command) 
            time.sleep(0.1)
            command = ':OUTP:OCP:VALue 3'
            self.device.write(command)
            print(f"PSU {self.model} sets overcurrent value successfully")
        else:
            print(f"PSU {self.model} do not have command for setting overcurrent")

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
        return self.device.query(command, delay=0.1)

    def get_voltage(self):
        command = ':VOLT?'

        self.device.write(command)
        return self.device.query(command, delay=0.1)

    def measure_current(self):
        command = ':MEAS:CURR?'

        self.device.write(command)
        time.sleep(0.5)
        return self.device.query(command, delay=0.1)

    def measure_voltage(self):
        command = ':MEAS:VOLT?'

        self.device.write(command)
        time.sleep(0.5)
        return self.device.query(command, delay=0.1)

    def set_channel(self, channel):
        self.channel = channel
