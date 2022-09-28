import numpy as np
from PID import PID
from PSU import PSU
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field 

def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])


if __name__ == "__main__":

    desired_magnetic_field = get_desired_magnetic_field()

    SPD3303C = PSU('CH2', 'SPD3303C')

    coils = np.array(
        [
            coil_current_control('x', initial_magnetic_field['x']),
            coil_current_control('y', initial_magnetic_field['y']),
            coil_current_control('z', initial_magnetic_field['z'])])

    PID = np.array([PID(), PID(), PID()])

    for i in range(2):
        coils[i].set_current()
        PID[i].set_initial_current(coils[i].get_current())

        if coils[i].axis == 'y':
            SPD3303C.set_channel('CH1')
            SPD3303C.set_current(0)
            SPD3303C.set_voltage(30)
        elif coils[i].axis == 'z':
            SPD3303C.set_channel('CH2')
            SPD3303C.set_current(0)
            SPD3303C.set_voltage(30)

        PID[i].set_initial_current(coils[i].get_current)
        PID[i].set_reference_magnetic_field(desired_magnetic_field[i])

    while 1:
        # TODO: get measurements from magnetometer
        for i in range(2):
            PID[i].set_measured_magnetic_field(.01)
            PID[i].calculate_current()
            # if coils[i].axis == 'x':
            #     available_PSUs[i].set_current(0)
            #     available_PSUs[i].set_voltage(30)
            # elif coils[i].axis == 'y':
            #     available_PSUs[i].set_channel('CH1')
            #     available_PSUs[i].set_current(0)
            #     available_PSUs[i].set_voltage(30)
            # elif coils[i].axis == 'z':
            #     available_PSUs[i].set_channel('CH2')
            #     available_PSUs[i].set_current(0)
            #     available_PSUs[i].set_voltage(30)

            if coils[i].axis == 'y':
                SPD3303C.set_channel('CH1')
                SPD3303C.set_current(0)
                SPD3303C.set_voltage(30)
            elif coils[i].axis == 'z':
                SPD3303C.set_channel('CH2')
                SPD3303C.set_current(0)
                SPD3303C.set_voltage(30)