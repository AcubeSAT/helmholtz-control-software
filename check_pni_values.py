import serial
import time

def initialize_serial(port, baudrate=115200, timeout=1):
    """Initialize the serial connection."""
    ser = serial.Serial(port, baudrate, timeout=timeout)
    return ser

def send_command(ser, command):
    """Send a command to the device."""
    command += '\r'  # Append carriage return
    print(f"Sending command: {command}")
    ser.write(command.encode())

def read_response(ser):
    """Read the response from the device."""
    time.sleep(0.5)  # Wait for the response
    response = ser.read_all().decode().strip()
    print(f"Response: {response}")
    return response

def check_version(ser):
    """Check the version of the device."""
    send_command(ser, 'v')
    response = read_response(ser)
    print(f"Device Version: {response}")

def run_self_test(ser):
    """Run the self-test."""
    send_command(ser, 'B')
    response = read_response(ser)
    if response:
        print("Self-test Result:", response)
    else:
        print("No response received for self-test.")

def start_sensor(ser, sensor_id, data_rate):
    """Start the sensor with given ID and data rate."""
    command = f's {sensor_id},{data_rate}'
    send_command(ser, command)
    response = read_response(ser)
    print(f"Start Sensor Response: {response}")

def display_sensor_data(ser):
    """Toggle sensor data display on."""
    send_command(ser, 'D1')
    response = read_response(ser)
    print(f"Sensor Data Display Response: {response}")

def parse_magnetic_field_data(data):
    """Parse a single line of magnetic field data and return X, Y, Z values."""
    fields = data.split(',')
    if len(fields) >= 6 and fields[1].strip() == 'magnetic field':
        x_value = float(fields[2].strip())
        y_value = float(fields[3].strip())
        z_value = float(fields[4].strip())
        return x_value, y_value, z_value
    else:
        return None

def read_sensor_data(ser, duration=10):
    """Read sensor data for a specified duration in seconds."""
    end_time = time.time() + duration
    while time.time() < end_time:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            x_y_z_values = parse_magnetic_field_data(data)
            if x_y_z_values:
                x, y, z = x_y_z_values
                print(f"X-Axis: {x} µT")
                print(f"Y-Axis: {y} µT")
                print(f"Z-Axis: {z} µT")

def main():
    port = '/dev/ttyUSB0'  # Replace with the correct port for your device
    ser = initialize_serial(port)

    try:
        check_version(ser)
        run_self_test(ser)
        start_sensor(ser, sensor_id=2, data_rate=100)  # Based on the datasheet
        display_sensor_data(ser)
        read_sensor_data(ser, duration=10)  # Read sensor data for 10 seconds

    finally:
        ser.close()

if __name__ == "__main__":
    main()
