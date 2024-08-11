import serial
import time

def initialize_serial(port, baudrate=115200, timeout=1):
    """Initialize the serial connection."""
    ser = serial.Serial(port, baudrate, timeout=timeout)
    return ser

def send_command(ser, command, file):
    """Send a command to the device."""
    command += '\r'  # Append carriage return
    file.write(f"Sending command: {command}\n")
    ser.write(command.encode())

def read_response(ser, file):
    """Read the response from the device."""
    time.sleep(0.5)  # Wait for the response
    response = ser.read_all().decode().strip()
    file.write(f"Response: {response}\n")
    return response

def check_version(ser, file):
    """Check the version of the device."""
    send_command(ser, 'v', file)
    response = read_response(ser, file)
    file.write(f"Device Version: {response}\n")

def run_self_test(ser, file):
    """Run the self-test."""
    send_command(ser, 'B', file)
    response = read_response(ser, file)
    if response:
        file.write(f"Self-test Result: {response}\n")
    else:
        file.write("No response received for self-test.\n")

def start_sensor(ser, sensor_id, data_rate, file):
    """Start the sensor with given ID and data rate."""
    command = f's {sensor_id},{data_rate}'
    send_command(ser, command, file)
    response = read_response(ser, file)
    file.write(f"Start Sensor Response: {response}\n")

def display_sensor_data(ser, file):
    """Toggle sensor data display on."""
    send_command(ser, 'D1', file)
    response = read_response(ser, file)
    file.write(f"Sensor Data Display Response: {response}\n")

def parse_magnetic_field_data(data):
    """Parse a single line of magnetic field data and return X, Y, Z values."""
    fields = data.split(',')
    if len(fields) >= 6 and fields[1].strip() == 'magnetic field':
        try:
            x_value = float(fields[2].strip())
            y_value = float(fields[3].strip())
            z_value = float(fields[4].strip())
            return x_value, y_value, z_value
        except ValueError:
            return None
    return None

def read_sensor_data(ser, duration, file):
    """Read sensor data for a specified duration in seconds."""
    end_time = time.time() + duration
    while time.time() < end_time:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            x_y_z_values = parse_magnetic_field_data(data)
            if x_y_z_values:
                x, y, z = x_y_z_values
                file.write(f"Calibrated X-Axis: {x} µT\n")
                file.write(f"Calibrated Y-Axis: {y} µT\n")
                file.write(f"Calibrated Z-Axis: {z} µT\n")

def main():
    port = '/dev/ttyUSB0'  # Replace with the correct port for your device
    ser = initialize_serial(port)
    
    # Open the text file for writing, which clears its previous content
    with open("output.txt", "w") as file:
        try:
            check_version(ser, file)
            run_self_test(ser, file)
            start_sensor(ser, sensor_id=2, data_rate=200, file=file)  
            display_sensor_data(ser, file)
            read_sensor_data(ser, duration=10, file=file)  # Read sensor data for 10 seconds

        finally:
            ser.close()

if __name__ == "__main__":
    main()
