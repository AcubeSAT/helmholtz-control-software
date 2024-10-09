import numpy as np
import time

import helmholtz_constants
from PSU import PSU
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field
from magnetometer import magnetometer
from magnetometer import PNI_magnetometer
from h_bridge import sent_sign
from scipy import constants

def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    print("Successfully got desired magnetic field")
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])   #converting microteslas to teslas


def get_initial_magnetic_field(magnetometer):
    # Needs almost five iretations in order to take the correct values from magnetometer
    for i in range(5):
        initial_field = magnetometer.read_sensor_data()
    return initial_field


if __name__ == "__main__":

    desired_magnetic_field = get_desired_magnetic_field()
    
    # Initialize magnetometer
    II2MDC = magnetometer.Magnetometer(port='/dev/ttyACM1')
    # magnetometer = PNI_magnetometer.PNI_magnetometer(port='/dev/ttyUSB0')
    # magnetometer.run_self_test()
    # magnetometer.start_sensor(sensor_id=2, data_rate=100)
    # magnetometer.display_sensor_data()

    # Initialize PSUs
    SPD3303C = PSU('CH1', 'SPD3303C')
    time.sleep(0.1)
    DP712 = PSU("CH1", 'DP712')
    time.sleep(0.1)
    DP712.set_overcurrent_protection()

    # Initialize magnetic field values from magnetometer
    helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = II2MDC.get_magnetic_field
    print(f"Initial magnetic field: {helmholtz_constants.initial_magnetic_field}")

    coils = np.array(
        [
            coil_current_control('x', initial_magnetic_field['x']),
            coil_current_control('y', initial_magnetic_field['y']),
            coil_current_control('z', initial_magnetic_field['z'])])

    print("Successful initialization")

    # Reset PSU to initial condition and set them ready for usage
    for i in range(3):
        coils[i].set_current()
        if coils[i].axis == 'y':
            SPD3303C.set_channel('CH1')
            time.sleep(0.1)
            SPD3303C.set_current(0)
            time.sleep(0.1)
            SPD3303C.set_voltage(30)
            time.sleep(0.1)
        elif coils[i].axis == 'z':
            SPD3303C.set_channel('CH2')
            time.sleep(0.1)
            SPD3303C.set_current(0)
            time.sleep(0.1)
            SPD3303C.set_voltage(30)
            time.sleep(0.1)
        else:
            time.sleep(0.1)
            DP712.set_current(0)
            time.sleep(0.1)
            DP712.set_voltage(30)
            time.sleep(0.1)

    print("Reset PSU current and voltage")

    # Sets the desired current values to PSUs, based on the desired magnetic field and sends the desired commands to rele
    for i in range(3):
        coils[i].set_desired_magnetic_field(desired_magnetic_field[i])
        coils[i].set_current()
        if coils[i].axis == 'y':
            SPD3303C.set_channel('CH1')
            time.sleep(0.1)
            SPD3303C.set_current(abs(coils[i].get_current()))
            time.sleep(0.1)
            if coils[i].get_current() >= 0:
                sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
            elif coils[i].get_current() < 0:
                sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
        elif coils[i].axis == 'z':
            SPD3303C.set_channel('CH2')
            time.sleep(0.1)
            SPD3303C.set_current(abs(coils[i].get_current()))
            time.sleep(0.1)
            if coils[i].get_current() >= 0:
                sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
            elif coils[i].get_current() < 0:
                sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
        else:
            time.sleep(0.1)
            DP712.set_current(abs(coils[i].get_current()))
            time.sleep(0.1)
            if coils[i].get_current() >= 0:
                sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
            elif coils[i].get_current() < 0:
                sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])    

    print("Successfully set current to PSUs and send current sign to rele")

    # Sets the desired current values to PSUs hardcoded, without transormation using magnetic field and sends the desired commands to rele
    # value_zero = 0
    # value_desired = 1
    # for i in range(3):
    #     if coils[i].axis == 'y':
    #         coils[i].set_current_hardcoded(0.350)
    #         SPD3303C.set_channel('CH1')
    #         time.sleep(0.1)
    #         SPD3303C.set_current(abs(coils[i].get_current()))
    #         time.sleep(0.1)
    #         if coils[i].get_current() >= 0:
    #             sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
    #         elif coils[i].get_current() < 0:
    #             sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
    #     elif coils[i].axis == 'z':
    #         coils[i].set_current_hardcoded(0.590)
    #         SPD3303C.set_channel('CH2')
    #         time.sleep(0.1)
    #         SPD3303C.set_current(abs(coils[i].get_current()))
    #         time.sleep(0.1)
    #         if coils[i].get_current() >= 0:
    #             sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
    #         elif coils[i].get_current() < 0:
    #             sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
    #     else:
    #         coils[i].set_current_hardcoded(0.05)
    #         DP712.set_current(abs(coils[i].get_current()))
    #         time.sleep(0.1)
    #         if coils[i].get_current() >= 0:
    #             sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
    #         elif coils[i].get_current() < 0:
    #             sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])    

    # print("Successfully set current to PSUs and send current sign to rele")

    # Prints magnetic field values and norm of the magnetic field
    while 1:
        magnetic_field = PNI_magnetometer.read_sensor_data()
        norm = np.sqrt(magnetic_field[0] ** 2 + magnetic_field[1] ** 2 + magnetic_field[2] ** 2)
        print(f"Magnetic field: {PNI_magnetometer.read_sensor_data()} Norm: {norm}")
    
        # Get the norm of the initial field
        magnetic_field = II2MDC.get_magnetic_field()
        initial_norm = np.sqrt(magnetic_field[0] ** 2 + magnetic_field[1] ** 2 + magnetic_field[2] ** 2)
        print(f"Magnetic field: {magnetic_field} Norm: {norm}")

