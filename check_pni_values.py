import serial

RM3100_RESET_CMD = bytes([0xA5, 0x04, 0x00, 0x00, 0x00, 0x00, 0x59])
RM3100_MAG_CMD = bytes([0xA5, 0x05, 0x00, 0x00, 0x00, 0x00, 0x59])

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)

# Send reset command
ser.write(RM3100_RESET_CMD)
print("Reset command sent")

# Wait for 1 second
import time
time.sleep(1)

# Send command to read magnetometer values
ser.write(RM3100_MAG_CMD)
print("Magnetometer read command sent")

# Read response
response = ser.read(7)

# Print raw response data
print("Raw response:", response)

# Extract magnetometer values from response
if response:
    mx = int.from_bytes(response[1:3], byteorder='little')
    my = int.from_bytes(response[3:5], byteorder='little')
    mz = int.from_bytes(response[5:7], byteorder='little')
    print(f"Magnetometer values: mx = {mx}, my = {my}, mz = {mz}")
else:
    print("No response received")

ser.close()