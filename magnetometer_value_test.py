# from magnetometer import magnetometer
# import time

# II2MDC = magnetometer.Magnetometer()
# while True:
#     print(II2MDC.get_magnetic_field())
#     time.sleep(0.1)

from magnetometer import magnetometer
import time
import numpy as np
import matplotlib.pyplot as plt

II2MDC = magnetometer.Magnetometer()

# Initialize lists to store magnetic field values and timestamps
timestamps = []
magnetic_field_value_array = []  # Stores [x, y, z] values for each timestamp
duration = 40  # Collect data for 40 seconds

# Start collecting data
start_time = time.time()
while True:

    current_time = time.time() - start_time
    
    if current_time > duration:
        break
    
    timestamps.append(current_time)

    # Get current magnetic field values (x, y, z)
    magnetic_field = II2MDC.get_magnetic_field()
    print(magnetic_field)

    # Add the current magnetic field values to the array
    magnetic_field_value_array.append(magnetic_field)

    # Sleep to prevent overwhelming the system
    time.sleep(0.1)

# Convert magnetic_field_value_array to numpy array for easier manipulation
magnetic_field_value_array = np.array(magnetic_field_value_array)

# Plotting
axes = ['x', 'y', 'z']
colors = ['r', 'g', 'b']

# Additional Plot: Measured Magnetic Field
fig, axs = plt.subplots(3, 1, figsize=(12, 18))  # Three separate subplots for x, y, z axes

for i in range(3):
    # Plot measured field
    axs[i].plot(timestamps, magnetic_field_value_array[:, i], label=f"Measured {axes[i]}-axis", color=colors[i])

    # Formatting
    axs[i].set_xlabel('Time (s)')
    axs[i].set_ylabel('Magnetic Field (µT)')
    axs[i].set_title(f'Measured Magnetic Field - {axes[i].upper()} Axis')
    axs[i].legend()
    axs[i].grid(True)

plt.tight_layout()
plt.show()
