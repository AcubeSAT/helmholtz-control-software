import numpy as np
import time
import matplotlib.pyplot as plt

import helmholtz_constants
from PSU import PSU
from PID import PID
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field
from magnetometer import magnetometer
from h_bridge import sent_sign
from Current_Magnetic_Field_Transform import input_magnetic_field_output_current


def get_desired_magnetic_field():
    """
    Prompts the user to input the desired magnetic field for each axis in microteslas (µT)
    and converts the input to teslas (T).
    """
    print('Command desired magnetic field for each axis in µT (e.g., "10 20 30"): ')
    try:
        desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    except ValueError:
        print("Invalid input. Please enter three numerical values separated by spaces.")
        return get_desired_magnetic_field()
    print("Successfully got desired magnetic field")
    return np.array([
        desired_magnetic_field_uT_x * 1e-6,
        desired_magnetic_field_uT_y * 1e-6,
        desired_magnetic_field_uT_z * 1e-6
    ])  # Converting microteslas to teslas


def main():
    # Initialize lists for saving data
    timestamps = []
    magnetic_field_error_list = []
    magnetic_field_value_list = []
    current_value_list = []

    # Get desired magnetic field from user
    desired_magnetic_field = get_desired_magnetic_field()

    # Duration to run the loop (in seconds)
    duration = 10

    # Initialize magnetometer
    II2MDC = magnetometer.Magnetometer(port='/dev/ttyACM1')

    # Initialize PSUs
    # SPD3303C = PSU('CH1', 'SPD3303C')
    # time.sleep(0.1)
    DP712 = PSU("CH1", 'DP712')
    # time.sleep(0.1)
    DP712.set_overcurrent_protection()

    # Initialize magnetic field values from magnetometer
    initial_field = None
    for _ in range(5):
        initial_field = II2MDC.get_magnetic_field() * 1e-6
        time.sleep(0.1)  # Slight delay between readings to ensure accurate measurements

    helmholtz_constants.initial_magnetic_field['x'] = initial_field[0]
    helmholtz_constants.initial_magnetic_field['y'] = initial_field[1]
    helmholtz_constants.initial_magnetic_field['z'] = initial_field[2]
    print(f"Initial magnetic field: {helmholtz_constants.initial_magnetic_field}")

    # Initialize coil controllers
    coils = np.array([
        coil_current_control('x', desired_magnetic_field[0], helmholtz_constants.initial_magnetic_field['x']),
        coil_current_control('y', desired_magnetic_field[1], helmholtz_constants.initial_magnetic_field['y']),
        coil_current_control('z', desired_magnetic_field[2], helmholtz_constants.initial_magnetic_field['z'])
    ])

    K_p = 160 * 1e-3
    K_d = 30 * 1e-3
    K_dd = 2 * 1e-3
    # Initialize PID controllers for each axis
    pid_controllers = [PID(K_p, K_d, K_dd), PID(K_p, K_d, K_dd), PID(K_p, K_d, K_dd)]

    # Retrieve coil lengths or relevant parameters
    coils_length = list(helmholtz_constants.coils.values())

    # Initialize instances for saving data
    magnetic_field_error_instance = [0, 0, 0]
    current_value_instance = [0, 0, 0]
    magnetic_field_value_instance = [0, 0, 0]

    print("Successful initialization")

    # Reset PSU to initial condition and set them ready for usage
    for i in range(3):
        # coils[i].set_current()
        if coils[i].axis == 'y':
            # SPD3303C.set_channel('CH1')
            # time.sleep(0.1)
            # SPD3303C.set_current(0)
            # time.sleep(0.1)
            # SPD3303C.set_voltage(30)
            # time.sleep(0.1)
            continue
        elif coils[i].axis == 'z':
            # SPD3303C.set_channel('CH2')
            # time.sleep(0.1)
            # SPD3303C.set_current(0)
            # time.sleep(0.1)
            # SPD3303C.set_voltage(30)
            # time.sleep(0.1)
            continue
        else:
            DP712.set_current(0)
            time.sleep(0.1)
            DP712.set_voltage(30)
            time.sleep(0.1)

        # Set reference current for PID controllers
        # Assuming input_magnetic_field_output_current returns the required current
        pid_controllers[i].set_desired_mf(desired_magnetic_field[i])
        pid_controllers[i].update_errors()
        magnetic_field_value_instance[i] = initial_field[i]
        magnetic_field_error_instance[i] = initial_field[i] - desired_magnetic_field[i]
        current_value_instance[i] = 0

    # Save the first set of data after all the initializations
    magnetic_field_value_list.append(magnetic_field_value_instance.copy())
    magnetic_field_error_list.append(magnetic_field_error_instance.copy())
    current_value_list.append(current_value_instance.copy())
    
    print("Reset PSU current and voltage")

    print(f"Starting measurement loop for {duration} seconds...")

    # Record the start time
    start_time = time.time()

    timestamps.append(0)

    try:
        while True:

            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > duration:
                print("Measurement duration completed.")
                break

            # Update PID controllers and set PSU currents
            for i in range(3):
                pid_controllers[i].calculate_mf()
                pid_controllers[i].set_measured_current(input_magnetic_field_output_current(pid_controllers[i].get_mf_control(), coils_length[i]))
                # print(pid_controllers[i].get_current_measured())

                # Set PSU current and sign based on the axis
                if coils[i].axis == 'y':
                    # SPD3303C.set_channel('CH1')
                    # # time.sleep(0.1)
                    # SPD3303C.set_current(abs(PID[i].get_current()))
                    # # time.sleep(0.1)
                    # if PID[i].get_current() >= 0:
                    #     sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
                    # elif PID[i].get_current() < 0:
                    #     sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
                    continue
                elif coils[i].axis == 'z':
                    # SPD3303C.set_channel('CH2')
                    # # time.sleep(0.1)
                    # SPD3303C.set_current(abs(PID[i].get_current()))
                    # # time.sleep(0.1)
                    # if PID[i].get_current() >= 0:
                    #     sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
                    # elif PID[i].get_current() < 0:
                    #     sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
                    continue
                else:
                    # time.sleep(0.1)
                    DP712.set_current(abs(pid_controllers[i].get_measured_current()))
                    # time.sleep(0.1)
                    if pid_controllers[i].get_measured_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
                    elif pid_controllers[i].get_measured_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])

            # Get new values from magnetometer
            magnetic_field_measured = II2MDC.get_magnetic_field() * 1e-6

            # Update PID controllers with measured data
            for i in range(3):
                pid_controllers[i].set_measured_mf(magnetic_field_measured[i])
                pid_controllers[i].update_errors()

                # Update data instances
                magnetic_field_value_instance[i] = pid_controllers[i].get_measured_mf()
                magnetic_field_error_instance[i] = pid_controllers[i].get_measured_mf() - pid_controllers[i].get_desired_mf()
                current_value_instance[i] = pid_controllers[i].get_measured_current()

            # Save the current timestamp and data
            timestamps.append(elapsed_time)
            magnetic_field_value_list.append(magnetic_field_value_instance.copy())
            magnetic_field_error_list.append(magnetic_field_error_instance.copy())
            current_value_list.append(current_value_instance.copy())

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Measurement interrupted by user.")

    # Convert lists to NumPy arrays for easier manipulation
    magnetic_field_value_array = np.array(magnetic_field_value_list)
    magnetic_field_error_array = np.array(magnetic_field_error_list)
    current_value_array = np.array(current_value_list) 
    timestamps = np.array(timestamps)

    DP712.set_current(0)
    time.sleep(0.1)
    DP712.set_voltage(0)
    time.sleep(0.1)

    # Plot magnetic field values
    plt.figure(figsize=(12, 8))

    # Magnetic Field X
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, magnetic_field_value_array[:, 0] * 1e6, label='Measured Magnetic Field X (\u03bcT)', color='r')
    plt.axhline(y=desired_magnetic_field[0] * 1e6, color='r', linestyle='--', label='Desired Magnetic Field X (\u03bcT)')
    plt.title('Magnetic Field X Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Y
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, magnetic_field_value_array[:, 1] * 1e6, label='Measured Magnetic Field Y (\u03bcT)', color='g')
    plt.axhline(y=desired_magnetic_field[1] * 1e6, color='g', linestyle='--', label='Desired Magnetic Field Y (\u03bcT)')
    plt.title('Magnetic Field Y Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Z
    plt.subplot(3, 1, 3)
    plt.plot(timestamps, magnetic_field_value_array[:, 2] * 1e6, label='Measured Magnetic Field Z (\u03bcT)', color='b')
    plt.axhline(y=desired_magnetic_field[2] * 1e6, color='b', linestyle='--', label='Desired Magnetic Field Z (\u03bcT)')
    plt.title('Magnetic Field Z Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Plot magnetic field values
    plt.figure(figsize=(12, 8))

    # Magnetic Field X
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, magnetic_field_error_array[:, 0] * 1e6, label='Error Magnetic Field X (\u03bcT)', color='r')
    plt.title('Error Magnetic Field X Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Error Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Y
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, magnetic_field_error_array[:, 1] * 1e6, label='Error Magnetic Field Y (\u03bcT)', color='g')
    plt.title('Error Magnetic Field Y Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Error Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Z
    plt.subplot(3, 1, 3)
    plt.plot(timestamps, magnetic_field_error_array[:, 2] * 1e6, label='Error Magnetic Field Z (\u03bcT)', color='b')
    plt.title('Error Magnetic Field Z Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Error Magnetic Field (\u03bcT)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Plot magnetic field values
    plt.figure(figsize=(12, 8))

    # Magnetic Field X
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, current_value_array[:, 0], label='Current X (\u03bcT)', color='r')
    plt.title('Current X Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Y
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, current_value_array[:, 1], label='Current Y (\u03bcT)', color='g')
    plt.title('Current Y Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (\u03bcT)')
    plt.grid()
    plt.legend()

    # Magnetic Field Z
    plt.subplot(3, 1, 3)
    plt.plot(timestamps, current_value_array[:, 2], label='Current Z (\u03bcT)', color='b')
    plt.title('Current Z Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (\u03bcT)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
