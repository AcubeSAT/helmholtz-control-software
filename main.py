import numpy as np
from PID import PID
from coil_current_control import coil_current_control


def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(int, input().split())
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])


if __name__ == "__main__":

    desired_magnetic_field = get_desired_magnetic_field()

    coils = np.array(
        [coil_current_control('x', desired_magnetic_field[0]),
         coil_current_control('y', desired_magnetic_field[1]),
         coil_current_control('z', desired_magnetic_field[2])])

    PID = np.array([PID(), PID(), PID()])

    for i in range(3):
        coils[i].initialize_PSU()
        coils[i].initial_current()
        PID[i].set_initial_current(coils[i].current)
        PID[i].set_reference_magnetic_field(desired_magnetic_field[i])

    while 1:
        # TODO: get measurements from magnetometer
        for i in range(3):
            PID[i].get_measured_magnetic_field(1)
            PID[i].calculate_current()
            coils[i].command_PSU_current(PID[i].current)
