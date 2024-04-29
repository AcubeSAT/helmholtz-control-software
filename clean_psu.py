import time
from PSU import PSU


if __name__ == "__main__":

    SPD3303C = PSU('CH2', 'SPD3303C')
    time.sleep(0.5)
    # DP712 = PSU("CH1", 'DP712')
    # time.sleep(0.5)

    # DP712.set_current(0)
    # time.sleep(0.2)
    # DP712.set_voltage(0)
    # time.sleep(0.2)

    SPD3303C.set_channel('CH1')
    time.sleep(0.2)
    SPD3303C.set_current(0)
    time.sleep(0.2)
    SPD3303C.set_voltage(0)
    time.sleep(0.2)

    # SPD3303C.set_channel('CH2')
    # time.sleep(0.2)
    # SPD3303C.set_current(0)
    # time.sleep(0.2)
    # SPD3303C.set_voltage(30)
    # time.sleep(0.2)