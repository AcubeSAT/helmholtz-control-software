import serial, time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)


def sent_sign(x):
    arduino.write(bytes(str(x), 'utf-8'))
    time.sleep(0.05)
#     data = arduino.readline()
#     return data
#
#
# while True:
#     num = 5
#     value = sent_sign(num)
#     print(value)
#
#     time.sleep(3)
#
#     num = -5
#     value = sent_sign(num)
#     print(value)
#
#     time.sleep(3)