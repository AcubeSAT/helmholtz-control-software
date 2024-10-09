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
from scipy import constants
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
    current_error_list = []
    magnetic_field_error_list = []
    current_value_list = []
    magnetic_field_value_list = []

    # Get desired magnetic field from user
    desired_magnetic_field = get_desired_magnetic_field()

    # Record the start time
    start_time = time.time()

    # Duration to run the loop (in seconds)
    duration = 30  # You can modify this as needed

    # Initialize magnetometer
    II2MDC = magnetometer.Magnetometer(port='/dev/ttyACM1')
    # Alternative magnetometer initialization (commented out)
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
    initial_field = None
    for _ in range(5):
        initial_field = II2MDC.get_magnetic_field()
        time.sleep(0.1)  # Slight delay between readings to ensure accurate measurements

    helmholtz_constants.initial_magnetic_field['x'] = initial_field[0]
    helmholtz_constants.initial_magnetic_field['y'] = initial_field[1]
    helmholtz_constants.initial_magnetic_field['z'] = initial_field[2]
    print(f"Initial magnetic field: {helmholtz_constants.initial_magnetic_field}")

    # Initialize coil controllers
    coils = np.array([
        coil_current_control('x', helmholtz_constants.initial_magnetic_field['x']),
        coil_current_control('y', helmholtz_constants.initial_magnetic_field['y']),
        coil_current_control('z', helmholtz_constants.initial_magnetic_field['z'])
    ])

    # Initialize PID controllers for each axis
    pid_controllers = [PID(), PID(), PID()]

    # Retrieve coil lengths or relevant parameters
    coils_length = list(helmholtz_constants.coils.values())

    # Initialize instances for saving data
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

        # Set reference current for PID controllers
        # Assuming input_magnetic_field_output_current returns the required current
        reference_current = input_magnetic_field_output_current(
            desired_magnetic_field[i] - initial_field[i],
            coils_length[i]
        )
        pid_controllers[i].set_reference_current(reference_current)
        pid_controllers[i].update_errors()
        current_value_instance[i] = pid_controllers[i].get_measured_current()
        magnetic_field_value_instance[i] = initial_field[i]
        current_error_instance[i] = pid_controllers[i].get_reference_current() - pid_controllers[i].get_measured_current()
        magnetic_field_error_instance[i] = desired_magnetic_field[i] - initial_field[i]

    # Save the first set of data after all the initializations
    current_value_list.append(current_value_instance.copy())
    magnetic_field_value_list.append(magnetic_field_value_instance.copy())
    current_error_list.append(current_error_instance.copy())
    magnetic_field_error_list.append(magnetic_field_error_instance.copy())
    timestamps.append(0)

    print("Reset PSU current and voltage")

    print(f"Starting measurement loop for {duration} seconds...")

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > duration:
                print("Measurement duration completed.")
                break

            # Update PID controllers and set PSU currents
            for i in range(3):
                pid_controllers[i].calculate_current()

                # Set PSU current and sign based on the axis
                if coils[i].axis == 'y':
                    SPD3303C.set_channel('CH1')
                    # time.sleep(0.1)
                    SPD3303C.set_current(abs(PID[i].get_current()))
                    # time.sleep(0.1)
                    if PID[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
                    elif PID[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
                elif coils[i].axis == 'z':
                    SPD3303C.set_channel('CH2')
                    # time.sleep(0.1)
                    SPD3303C.set_current(abs(PID[i].get_current()))
                    # time.sleep(0.1)
                    if PID[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
                    elif PID[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
                else:
                    # time.sleep(0.1)
                    DP712.set_current(abs(PID[i].get_current()))
                    # time.sleep(0.1)
                    if PID[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
                    elif PID[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])

            # Get new values from magnetometer
            magnetic_field_measured = II2MDC.get_magnetic_field()

            # Calculate norm of the magnetic field
            norm_magnetic_field = np.linalg.norm(magnetic_field_measured)
            print(f"Magnetic field: {magnetic_field_measured}   Norm: {norm_magnetic_field:.6f} T")

            # Update PID controllers with measured data
            for i in range(3):
                # Calculate the measured magnetic field relative to initial field
                measured_field_relative = magnetic_field_measured[i] - initial_field[i]
                # Convert measured magnetic field error to current (assuming input_magnetic_field_output_current handles this)
                measured_current = input_magnetic_field_output_current(measured_field_relative, coils_length[i])
                pid_controllers[i].set_measured_current(measured_current)
                pid_controllers[i].update_errors()

                # Update data instances
                current_value_instance[i] = pid_controllers[i].get_measured_current()
                magnetic_field_value_instance[i] = magnetic_field_measured[i]
                current_error_instance[i] = pid_controllers[i].get_reference_current() - pid_controllers[i].get_measured_current()
                magnetic_field_error_instance[i] = desired_magnetic_field[i] - magnetic_field_measured[i]

            # Save the current timestamp and data
            timestamps.append(elapsed_time)
            current_value_list.append(current_value_instance.copy())
            magnetic_field_value_list.append(magnetic_field_value_instance.copy())
            current_error_list.append(current_error_instance.copy())
            magnetic_field_error_list.append(magnetic_field_error_instance.copy())

            # Control loop frequency (10 Hz)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Measurement interrupted by user.")

    # Convert lists to NumPy arrays for easier manipulation
    current_value_array = np.array(current_value_list)  # Shape: (num_samples, 3)
    magnetic_field_value_array = np.array(magnetic_field_value_list)  # Shape: (num_samples, 3)
    current_error_array = np.array(current_error_list)  # Shape: (num_samples, 3)
    magnetic_field_error_array = np.array(magnetic_field_error_list)  # Shape: (num_samples, 3)
    timestamps = np.array(timestamps)

    # Plotting
    # Plot magnetic field values
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, magnetic_field_value_array[:, 0], label='Magnetic Field X (T)', color='r')
    plt.title('Magnetic Field X Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (T)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, magnetic_field_value_array[:, 1], label='Magnetic Field Y (T)', color='g')
    plt.title('Magnetic Field Y Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (T)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, magnetic_field_value_array[:, 2], label='Magnetic Field Z (T)', color='b')
    plt.title('Magnetic Field Z Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field (T)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Plot current values
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, current_value_array[:, 0], label='Current X (A)', color='r')
    plt.title('Current X Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, current_value_array[:, 1], label='Current Y (A)', color='g')
    plt.title('Current Y Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, current_value_array[:, 2], label='Current Z (A)', color='b')
    plt.title('Current Z Axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
