import serial
import time

# Set the serial port and baud rate
serial_port = '/dev/ttyUSB0'
baud_rate = 115200

# Set the command to send to the sensor
command = '?\r\n'

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Send the command to the sensor
# ...

# Send the command to the sensor
ser.write(command.encode())

# Wait for a response from the sensor
response = ser.readline()

# Check if the sensor responded
if response:
    print(f'Sensor responded with: {response}')
    print(f'Response length: {len(response)}')
    print(f'Response type: {type(response)}')
    print(f'Response hex: {response.hex()}')
else:
    print('Sensor did not respond')