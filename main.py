from PSU import PSU
import time
from coil_current_control import coil_current_control
from PID import PID
import helmholtz_constants

voltage_wanted = [1.0000, 1.1987, 1.3894, 1.5646, 1.7174, 1.8415, 1.9320, 1.9854, 1.9996, 1.9738, 1.9093, 1.8085,
                  1.6755, 1.5155, 1.3350, 1.1411, 0.9416, 0.7445, 0.5575, 0.3881, 0.2432, 0.1284, 0.0484, 0.0063,
                  0.0038, 0.0411, 0.1165, 0.2272, 0.3687, 0.5354, 0.7206, 0.9169, 1.0000]

frequency = 0.1  # in Hz (maximum 0.15 Hz)

time_to_sleep = 1 / (frequency * len(voltage_wanted))


def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(int, input().split())
    return desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6, desired_magnetic_field_uT_z * 10 ** -6


if __name__ == "__main__":

    desired_magnetic_field_x, desired_magnetic_field_y, desired_magnetic_field_z = get_desired_magnetic_field()

    coil_x = coil_current_control(axis='x', desired_magnetic_field=desired_magnetic_field_x)
    coil_x.initialize_PSU()
    coil_x.initial_current()

    PID_x = PID()
    PID_x.get_initial_current(coil_x.current)
    PID_x.get_reference_magnetic_field(desired_magnetic_field_x)

    coil_y = coil_current_control(axis='y', desired_magnetic_field=desired_magnetic_field_y)
    coil_y.initialize_PSU()
    coil_y.initial_current()

    PID_y = PID()
    PID_y.get_initial_current(coil_y.current)
    PID_y.get_reference_magnetic_field(desired_magnetic_field_y)

    coil_z = coil_current_control(axis='z', desired_magnetic_field=desired_magnetic_field_z)
    # coil_z.initialize_PSU()
    coil_z.initial_current()

    PID_z = PID()
    PID_z.get_initial_current(coil_z.current)
    PID_z.get_reference_magnetic_field(desired_magnetic_field_z)

    while 1:
        PID_x.get_measured_magnetic_field(1)
        PID_x.calculate_current()
        coil_x.command_PSU_current(PID_x.current)

        PID_y.get_measured_magnetic_field(1)
        PID_y.calculate_current()
        coil_y.command_PSU_current(PID_y.current)

        PID_z.get_measured_magnetic_field(1)
        PID_z.calculate_current()
        coil_z.command_PSU_current(PID_x.current)


