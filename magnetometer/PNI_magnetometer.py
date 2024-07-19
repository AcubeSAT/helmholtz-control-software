import serial
import time

class PNI_magnetometer:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        """Initialize the serial connection."""
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        """Send a command to the device and return its response."""
        command += '\r'  # Append carriage return
        self.ser.write(command.encode())

    def read_response(self):
        """Read the response from the device."""
        time.sleep(0.05)  # Wait for the response
        response = self.ser.read_all().decode().strip()
        # print(f"Response: {response}")
        return response

    def check_version(self):
        """Check the version of the device."""
        self.send_command('v')
        response = self.read_response()
        print(f"Device Version: {response}")

    def run_self_test(self):
        """Run the self-test."""
        self.send_command('B')
        response = self.read_response()
        if response:
            print("Self-test completed")
            # print(f"Response of self-test is: {response}")
        else:
            print("No response received for self-test.")

    def start_sensor(self, sensor_id, data_rate):
        """Start the sensor with given ID and data rate."""
        command = f's {sensor_id},{data_rate}'
        self.send_command(command)
        response = self.read_response()
        if response:
            print("Sensor has started successfully")
            # print(f"Start Sensor Response: {response}")
        else:
            print("Sensor could NOT start")

    def display_sensor_data(self):
        """Toggle sensor data display on."""
        self.send_command('D1')
        print(f"Toggle sensor data display on")

    def parse_magnetic_field_data(self, data):
        """Parse a single line of magnetic field data and return X, Y, Z values."""
        fields = data.split(',')
        if len(fields) >= 6 and fields[1].strip() == 'magnetic field':
            # print(fields[2].strip())
            # print(fields[3].strip())
            # print(fields[4].strip())
            x_value = float(fields[2].strip())
            y_value = float(fields[3].strip())
            z_value = float(fields[4].strip())
            # magn_score = float(fields[5].strip())
            return x_value, y_value, z_value
        else:
            return None
    
    def read_sensor_data(self,):
        """Read sensor data for a specified duration in seconds."""
        while True:
            try:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode().strip()
                    x_y_z_values = self.parse_magnetic_field_data(data)
                    if x_y_z_values:
                        return x_y_z_values
            except:
                print("Wait for proper value format")

    def close(self):
        """Close the serial connection."""
        self.ser.close()
        print("Device closed successfully")
