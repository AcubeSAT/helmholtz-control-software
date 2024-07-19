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
    # II2MDC = magnetometer.Magnetometer(port='/dev/ttyACM1')
    magnetometer = PNI_magnetometer.PNI_magnetometer(port='/dev/ttyUSB0')
    magnetometer.run_self_test()
    magnetometer.start_sensor(sensor_id=2, data_rate=100)
    magnetometer.display_sensor_data()

    # Initialize PSUs
    SPD3303C = PSU('CH1', 'SPD3303C')
    time.sleep(0.1)
    DP712 = PSU("CH1", 'DP712')
    time.sleep(0.1)
    DP712.set_overcurrent_protection()

    # Initialize magnetic field values from magnetometer
    helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = get_initial_magnetic_field(magnetometer=PNI_magnetometer)
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

    # Calculate the theoretical field created by the helmholtz cage for each axis and the norm
    theoretical_magn = [0, 0, 0]
    for i in range(3):
        gamma = helmholtz_constants.beta / helmholtz_constants.coils[coils[i].axis]
        theoretical_magn[i] = coils[i].get_current() / (np.pi * helmholtz_constants.coils[coils[i].axis] / (
            2 * constants.mu_0 * helmholtz_constants.wire_turns) * (
                        (1 + gamma ** 2) * np.sqrt(2 + gamma ** 2)) / 2)
    theoretical_magn_norm = np.sqrt(theoretical_magn[0] ** 2 + theoretical_magn[1] ** 2 + theoretical_magn[2] ** 2)    

    # If you uncomment the next three lines you will take the values of current based on sensors at the output of PSU channels
    # print(SPD3303C.measure_current())
    # time.sleep(0.1)
    # print(DP712.measure_current())
    # time.sleep(0.1)

    # Prints magnetic field values and norm
    while 1:
        magnetic_field = PNI_magnetometer.read_sensor_data()
        norm = np.sqrt(magnetic_field[0] ** 2 + magnetic_field[1] ** 2 + magnetic_field[2] ** 2)
        print(f"Magnetic field: {PNI_magnetometer.read_sensor_data()} Norm: {norm}")
    
    # # Open the file in append mode
    # with open("magnetic_field.txt", "a") as file:
    #     # Writes magnetic field values and norm
    #     while True:
    #         magnetic_field = II2MDC.get_magnetic_field()
    #         norm = np.sqrt(magnetic_field[0] ** 2 + magnetic_field[1] ** 2 + magnetic_field[2] ** 2)
    #         print(f"Magnetic field: {magnetic_field} Norm: {norm}")
    #         file.write(f"Magnetic field: {magnetic_field} Norm: {norm}\n")

        # # Calculate noise in each axis and the norm
        # noise_x = magnetic_field[0] * 1e-6 - initial_magnetic_field['x'] - theoretical_magn[0] 
        # noise_y = magnetic_field[1] * 1e-6 - initial_magnetic_field['y'] - theoretical_magn[1]
        # noise_z = magnetic_field[2] * 1e-6 - initial_magnetic_field['z'] - theoretical_magn[2]
        # noise_norm =  np.sqrt(noise_x ** 2 + noise_y ** 2 + noise_z** 2)
        # print(f"Magnetic field noise per axis, x:{noise_x}, y:{noise_y}, z:{noise_z} and Norm noise: {noise_norm}")

        # # Get the norm of the initial field
        # initial_norm = np.sqrt(initial_magnetic_field['x'] ** 2 + initial_magnetic_field['y'] ** 2 + initial_magnetic_field['z'] ** 2)
        # print(f"Magnetic field: {II2MDC.get_magnetic_field()} Norm: {norm}")

