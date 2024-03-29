import numpy as np
import time

import helmholtz_constants
from PID import PID
from PSU import PSU
from coil_current_control import coil_current_control
from magnetometer import magnetometer
from h_bridge import sent_sign
from Current_Magnetic_Field_Transform import input_magnetic_field_output_current


def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])

def get_initial_magnetic_field(magnetometer):
    for i in range(5):
        initial_field = magnetometer.get_magnetic_field() * 10 ** -6
    return initial_field


if __name__ == "__main__":

    desired_magnetic_field = get_desired_magnetic_field()
    II2MDC = magnetometer.Magnetometer()
    # loop to get the correct magnetometer values
    for _ in range(5):
        ambient_magnetic_field = II2MDC.get_magnetic_field()

    SPD3303C = PSU('CH2', 'SPD3303C')
    time.sleep(0.5)
    DP712 = PSU("CH1", 'DP712')

    helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = get_initial_magnetic_field(magnetometer=II2MDC)
    print(helmholtz_constants.initial_magnetic_field)
    # desired_magnetic_field =[1,1,1]
    coils = np.array(
        [
            coil_current_control('x', helmholtz_constants.initial_magnetic_field['x']),
            coil_current_control('y', helmholtz_constants.initial_magnetic_field['y']),
            coil_current_control('z', helmholtz_constants.initial_magnetic_field['z'])])

    PID = [PID(), PID(), PID()]

    coils_length = list(helmholtz_constants.coils.values())

    for i in range(3):
        coils[i].set_current()

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
            time.sleep(0.2)
        else:
            time.sleep(0.2)
            DP712.set_current(0)
            time.sleep(0.2)
            DP712.set_voltage(30)
            time.sleep(0.2)

        PID[i].set_reference_magnetic_field(desired_magnetic_field[i])
        PID[i].set_reference_current(input_magnetic_field_output_current(desired_magnetic_field[i] - ambient_magnetic_field[i], coils_length[i]))
        PID[i].update_errors()

    while 1:
        for i in range(3):
            PID[i].calculate_current()
            if coils[i].axis == 'y':
                SPD3303C.set_channel('CH1')
                time.sleep(0.1)
                SPD3303C.set_current(abs(PID[i].get_current()))
                time.sleep(0.1)
                if PID[i].get_current() >= 0:
                    sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
                elif PID[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
            elif coils[i].axis == 'z':
                SPD3303C.set_channel('CH2')
                time.sleep(0.1)
                SPD3303C.set_current(abs(PID[i].get_current()))
                time.sleep(0.1)
                if PID[i].get_current() >= 0:
                    sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
                elif PID[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
            else:
                time.sleep(0.1)
                DP712.set_current(abs(PID[i].get_current()))
                time.sleep(0.1)
                if PID[i].get_current() >= 0:
                    sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])
                elif PID[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])

        magnetic_field_measured = II2MDC.get_magnetic_field()
        for i in range(3):
            PID[i].set_measured_current(input_magnetic_field_output_current(magnetic_field_measured[i] - ambient_magnetic_field[i]))
            PID[i].update_errors()

        norm_magnetic_field = np.sqrt(magnetic_field_measured[0] ** 2 + magnetic_field_measured[1] ** 2 + magnetic_field_measured[2] ** 2)
        print(magnetic_field_measured, " ", norm_magnetic_field)
        time.sleep(0.1)

