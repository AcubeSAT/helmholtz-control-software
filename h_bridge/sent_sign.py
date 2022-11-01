import serial, time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)


def sent_sign(x):
    arduino.write(bytes(x))
    time.sleep(0.05)
    data = arduino.readline()
    arduino.flushOutput()
    return data

num = 3
index = 0

msg = b"\x10"
msg2 = b"\x11"
msg3 = b"\x20"
msg4 = b"\x21"
msg5 = b"\x30"
msg6 = b"\x31"

# while True:
#     pass
    # time.sleep(3)
    # arduino.write(msg)
    # time.sleep(3)
    # arduino.write(msg2)
    # time.sleep(3)
    # value = sent_sign(msg3)
    # print(msg3)
    # time.sleep(3)
    # value = sent_sign(msg4)
    # print(msg4)
    # time.sleep(3)
    #
    # value = sent_sign(msg5)
    # print(msg3)
    # time.sleep(3)
    #
    # value = sent_sign(msg6)
    # print(msg4)
    # time.sleep(3)

