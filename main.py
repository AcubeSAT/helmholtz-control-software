import numpy as np
import time

import helmholtz_constants
from PID import PID
from PSU import PSU
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field
from magnetometer import magnetometer
from h_bridge import sent_sign


def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])


def get_initial_magnetic_field(magnetometer):
    for i in range(5):
        initial_field = magnetometer.get_magnetic_field()
    return initial_field


if __name__ == "__main__":

    # desired_magnetic_field = get_desired_magnetic_field()
    # RM3100 = magnetometer.Magnetometer()
    # magnetometer_measurements = RM3100.get_magnetic_field()

    SPD3303C = PSU('CH2', 'SPD3303C')
    time.sleep(.5)
    DP712 = PSU("CH1", 'DP712')

    # helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = get_initial_magnetic_field(magnetometer=RM3100)
    desired_magnetic_field =[1,1,1]
    coils = np.array(
        [
            coil_current_control('x', initial_magnetic_field['x']),
            coil_current_control('y', initial_magnetic_field['y']),
            coil_current_control('z', initial_magnetic_field['z'])])

    PID = [PID(), PID(), PID()]

    for i in range(3):
        coils[i].set_current()
        PID[i].set_initial_current(coils[i].get_current())

        if coils[i].axis == 'y':
            SPD3303C.set_channel('CH1')
            time.sleep(0.2)
            SPD3303C.set_current(0)
            time.sleep(0.2)
            SPD3303C.set_voltage(30)
            time.sleep(0.2)
        elif coils[i].axis == 'z':
            SPD3303C.set_channel('CH2')
            time.sleep(0.2)
            SPD3303C.set_current(0)
            time.sleep(0.2)
            SPD3303C.set_voltage(30)
            time.sleep(.2)
        else:
            time.sleep(.2)
            DP712.set_current(0)
            time.sleep(.2)
            DP712.set_voltage(30)
            time.sleep(.2)
    #
    #     PID[i].set_initial_current(coils[i].get_current())
    #     PID[i].set_reference_magnetic_field(desired_magnetic_field[i])
    #
    coils[0].current = 0
    coils[1].current = -0.8
    coils[2].current = 1

    while 1:
        for i in range(3):
            time.sleep(0.1)
            coils[i].set_desired_magnetic_field(desired_magnetic_field[i])
            # coils[i].set_current()
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
                time.sleep(1)
                DP712.set_current(abs(coils[i].get_current()))
                time.sleep(0.2)
                if coils[i].get_current() >= 0:
                    sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
                elif coils[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])

        while 1:
            print(SPD3303C.measure_current())
            time.sleep(0.1)
            print(DP712.measure_current())
    # while 1:
    #     # TODO: get measurements from magnetometer
    #     for i in range(2):
    #         PID[i].set_measured_magnetic_field(.01)
    #         PID[i].calculate_current()
    #
    #         if coils[i].axis == 'y':
    #             SPD3303C.set_channel('CH1')
    #             SPD3303C.set_current(0)
    #             SPD3303C.set_voltage(30)
    #         elif coils[i].axis == 'z':
    #             SPD3303C.set_channel('CH2')
    #             SPD3303C.set_current(0)
    #             SPD3303C.set_voltage(30)
