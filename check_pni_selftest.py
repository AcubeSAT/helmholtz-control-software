import serial
import time

def initialize_serial(port, baudrate=115200, timeout=1):
    """Initialize the serial connection."""
    ser = serial.Serial(port, baudrate, timeout=timeout)
    return ser

def send_command(ser, command):
    """Send a command to the device."""
    command += '\r'  # Append carriage return
    ser.write(command.encode())

def read_response(ser):
    """Read the response from the device."""
    time.sleep(0.1)  # Wait for the response
    response = ser.read_all().decode().strip()
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

def main():
    port = '/dev/ttyUSB0'
    ser = initialize_serial(port)

    try:
        check_version(ser)
        run_self_test(ser)
        start_sensor(ser, sensor_id=2, data_rate=100)  
        display_sensor_data(ser)
    finally:
        ser.close()

if __name__ == "__main__":
    main()
