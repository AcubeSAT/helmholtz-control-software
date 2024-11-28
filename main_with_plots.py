import numpy as np
import time
import matplotlib.pyplot as plt

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
    desired_magnetic_field = get_desired_magnetic_field()

    # Initialize magnetometer
    II2MDC = magnetometer.Magnetometer()
    # magnetometer = PNI_magnetometer.PNI_magnetometer(port='/dev/ttyUSB0')
    # magnetometer.run_self_test()
    # magnetometer.start_sensor(sensor_id=2, data_rate=100)
    # magnetometer.display_sensor_data()

    # Initialize PSUs
    # SPD3303C = PSU('CH1', 'SPD3303C')
    # time.sleep(0.1)
    DP712 = PSU("CH1", 'DP712')
    time.sleep(0.1)
    DP712.set_overcurrent_protection()

    # Initialize magnetic field values from magnetometer

    # Initialize magnetic field values from magnetometer
    
    for i in range(20):
        initial_magnetic_field = II2MDC.get_magnetic_field()
    # initial_magnetic_field
    print(f"Initial magnetic field: {initial_magnetic_field}")

    coils = np.array(
        [
            coil_current_control('x', desired_magnetic_field[0], initial_magnetic_field[0] * 10 ** -6),
            coil_current_control('y', desired_magnetic_field[1], initial_magnetic_field[1] * 10 ** -6),
            coil_current_control('z', desired_magnetic_field[2], initial_magnetic_field[2] * 10 ** -6)])

    print("Successful initialization")

    # Reset PSU to initial condition and set them ready for usage
    for coil in coils:
        coil.set_current()
        if coil.axis == 'y':
            continue
            # SPD3303C.set_channel('CH1')
            # time.sleep(0.1)
            # SPD3303C.set_current(0)
            # time.sleep(0.1)
            # SPD3303C.set_voltage(30)
            # time.sleep(0.1)
        elif coil.axis == 'z':
            continue
            # SPD3303C.set_channel('CH2')
            # time.sleep(0.1)
            # SPD3303C.set_current(0)
            # time.sleep(0.1)
            # SPD3303C.set_voltage(30)
            # time.sleep(0.1)
        else:
            time.sleep(0.1)
            DP712.set_current(0)
            time.sleep(0.1)
            DP712.set_voltage(30)
            time.sleep(0.1)

    print("Reset PSU current and voltage")

    # Initialize data storage
    timestamps = []
    measured_fields = []

    # Record the start time
    start_time = time.time()

    # Duration to run the loop (in seconds)
    duration = 3

    print(f"Starting measurement loop for {duration} seconds...")

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > duration:
                print("Measurement duration completed.")
                break
            
             # Sets the desired current values to PSUs, based on the desired magnetic field and sends the desired commands to rele
            for i in range(3):
                coils[i].set_desired_magnetic_field (desired_magnetic_field[i])
                coils[i].set_current()
                if coils[i].axis == 'y':
                    continue
                    # SPD3303C.set_channel('CH1')
                    # time.sleep(0.1)
                    # SPD3303C.set_current(abs(coil.get_current()))
                    # time.sleep(0.1)
                    # if coil.get_current() >= 0:
                    #     sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
                    # else:
                    #     sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
                elif coils[i].axis == 'z':
                    continue
                    # SPD3303C.set_channel('CH2')
                    # time.sleep(0.1)
                    # SPD3303C.set_current(abs(coil.get_current()))
                    # time.sleep(0.1)
                    # if coil.get_current() >= 0:
                    #     sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
                    # else:
                    #     sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
                else:
                    # time.sleep(0.1)
                    DP712.set_current(abs(coils[i].get_current()))
                    # time.sleep(0.1)
                    if coils[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])
                    else:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])

            print("Successfully set current to PSUs and sent current sign to rele")

            # Read magnetic field
            magnetic_field = II2MDC.get_magnetic_field()
            norm = np.sqrt(np.sum(np.square(magnetic_field)))
            print(f"Magnetic field: {magnetic_field} Norm: {norm}")

            # Store the data
            timestamps.append(elapsed_time)
            measured_fields.append(magnetic_field.copy())

            # Optional: Sleep to control loop frequency (e.g., 10 Hz)
            # time.sleep(0.01)

    except KeyboardInterrupt:
        print("Measurement interrupted by user.")

    # Convert measured_fields to a NumPy array for easier manipulation
    measured_fields = np.array(measured_fields)  # Shape: (num_samples, 3)

    DP712.set_current(0)
    time.sleep(0.1)
    DP712.set_voltage(0)
    time.sleep(0.1)

    # Plotting
    axes = ['x', 'y', 'z']
    colors = ['r', 'g', 'b']

    fig, axs = plt.subplots(3, 1, figsize=(12, 18))  # Three separate subplots

    for i in range(3):
        axs[i].plot(timestamps, measured_fields[:, i], label=f"Measured {axes[i]}-axis", color=colors[i])
        axs[i].hlines(desired_magnetic_field[i] * 1e6, 0, duration, colors=colors[i], linestyles='dashed', label=f"Desired {axes[i]}-axis")
        axs[i].set_xlabel('Time (s)')
        axs[i].set_ylabel('Magnetic Field (µT)')
        axs[i].set_title(f'Helmholtz Cage Magnetic Field Response - {axes[i].upper()} Axis')
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
