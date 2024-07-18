import numpy as np
import time

import helmholtz_constants
from PSU import PSU
from PID import PID
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field
from magnetometer import magnetometer
from h_bridge import sent_sign
from scipy import constants
from Current_Magnetic_Field_Transform import input_magnetic_field_output_current

def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    print("Successfully got desired magnetic field")
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])   #converting microteslas to teslas

if __name__ == "__main__":

    # initialize lists for saving data
    current_error_list = []
    magnetic_field_error_list = []
    current_value_list = []
    magnetic_field_value_list = []

    desired_magnetic_field = get_desired_magnetic_field()
    
    # Initialize magnetometer
    II2MDC = magnetometer.Magnetometer()

    # Initialize PSUs
    SPD3303C = PSU('CH1', 'SPD3303C')
    time.sleep(0.1)
    DP712 = PSU("CH1", 'DP712')
    time.sleep(0.1)
    DP712.set_overcurrent_protection()


    # loop to get the correct magnetometer values
    for _ in range(5):
        ambient_magnetic_field = II2MDC.get_magnetic_field()

    # Initialize magnetic field values from magnetometer
    helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = ambient_magnetic_field

    coils = np.array(
        [
            coil_current_control('x', initial_magnetic_field['x']),
            coil_current_control('y', initial_magnetic_field['y']),
            coil_current_control('z', initial_magnetic_field['z'])])

    PID = [PID(), PID(), PID()]

    coils_length = list(helmholtz_constants.coils.values())

    # initialize instances for saving data
    current_error_instance = [0, 0, 0]
    magnetic_field_error_instance = [0, 0, 0]
    current_value_instance = [0, 0, 0]
    magnetic_field_value_instance = [0, 0, 0]

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

        PID[i].set_reference_current(input_magnetic_field_output_current(desired_magnetic_field[i] - ambient_magnetic_field[i], coils_length[i]))
        PID[i].update_errors()
        current_value_instance[i] = PID[i].get_measured_current()
        magnetic_field_value_instance[i] = ambient_magnetic_field[i]
        current_error_instance[i] = PID[i].get_reference_current() - PID[i].get_measured_current()
        magnetic_field_error_instance[i] = desired_magnetic_field[i] - ambient_magnetic_field[i]

    # save the first set of data after all the initializations
    current_value_list.append(current_value_instance)
    magnetic_field_value_list.append(magnetic_field_value_instance)
    current_error_list.append(current_error_instance)
    magnetic_field_error_list.append(magnetic_field_error_instance)

    print("Reset PSU current and voltage")

    #NOTE: The time of sleep is huge for a proper control loop, play with it nad try to tue it
    # Sets the desired current values to PSUs, based on the desired magnetic field and sends the desired commands to rele
    while 1:
        # calculate current from PID, send absolute value of this current to PSU and send the sign of the current value to arduino
        for i in range(3):
            PID[i].calculate_current()
            if coils[i].axis == 'y':
                SPD3303C.set_channel('CH1')
                time.sleep(0.1)
                SPD3303C.set_current(abs(PID[i].get_current()))
                time.sleep(0.1)
                if PID[i].get_current() >= 0:
                    sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
                elif PID[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
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
                    sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
                elif PID[i].get_current() < 0:
                    sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])

        # get new values from magnetometer, update the PID and save the data
        magnetic_field_measured = II2MDC.get_magnetic_field()
        for i in range(3):
            PID[i].set_measured_current(input_magnetic_field_output_current(magnetic_field_measured[i] - ambient_magnetic_field[i]))
            PID[i].update_errors()
            current_value_instance[i] = PID[i].get_measured_current()
            magnetic_field_value_instance[i] = magnetic_field_measured[i]
            current_error_instance[i] = PID[i].get_reference_current() - PID[i].get_measured_current()
            magnetic_field_error_instance[i] = desired_magnetic_field[i] - magnetic_field_measured[i]

        # save the first set of data after all the initializations
        current_value_list.append(current_value_instance)
        magnetic_field_value_list.append(magnetic_field_value_instance)
        current_error_list.append(current_error_instance)
        magnetic_field_error_list.append(magnetic_field_error_instance)
        
        # calculate the norm of magnetic field and print the magnetic field per axis and the norm of it
        norm_magnetic_field = np.sqrt(magnetic_field_measured[0] ** 2 + magnetic_field_measured[1] ** 2 + magnetic_field_measured[2] ** 2)
        print(magnetic_field_measured, "   ", norm_magnetic_field)
        time.sleep(0.1)