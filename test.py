from magnetometer import magnetometer
import time

II2MDC = magnetometer.Magnetometer()
while True:
    print(II2MDC.get_magnetic_field())
    # time.sleep(0.1)