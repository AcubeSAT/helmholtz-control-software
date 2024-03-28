import numpy as np

""" Magnetic Field Parameters """

# Preferred magnetic field in SI values
mag_ref = np.array([20 * 1e-6, 30 * 1e-6, 15 * 1e-6])

# create noise array using randomness (length = samples)
# noise[0] is noise at x axis
# noise[1] is noise at y axis
# noise[2] is noise at z axis
noise = np.random.normal(0, 15 * 1e-9, 3)

""" Coil Parameters """

# length of the side of the coils
# SIDE_LEN[0] is for the x-axis
# SIDE_LEN[1] is for the y-axis
# SIDE_LEN[2] is for the z-axis
SIDE_LEN = [1.65, 1.70, 1.75]

# resistance of the coils
# RES[0] is for the x-axis
# RES[1] is for the y-axis
# RES[2] is for the z-axis
RES = [2.5, 2.6, 2.9]

# set controller's gains for x-axis
# k_x[0] = kp
# k_x[1] = kd
# k_x[2] = ki
K_x = np.array([0.4, 0.2, 0.24])
# set controller's gains for y-axis
# k_y[0] = kp
# k_y[1] = kd
# k_y[2] = ki
K_y = np.array([0.3, 0.13, 0.24])
# set controller's gains for z-axis
# k_z[0] = kp
# k_z[1] = kd
# k_z[2] = ki
K_z = np.array([0.15, 0.2, 0.23])

# length of the coil
LENGTH = 6 * 1e-2

# the number of wire turns in each coil
WIRE_TURNS = 50

# magnetic permeability of air
MAG_PERM = 4 * np.pi * 1e-7

""" Optimal_Gain_Values Testing Parameters """

# Kp[0]: starting value of kp gain
# Kp[1]: ending value of kp gain
# Kp[2]: increasing step of kp gain
Kp = [0.1, 0.4, 0.01]

# Kd[0]: starting value of kd gain
# Kd[1]: ending value of kd gain
# Kd[2]: increasing step of kd gain
Kd = [0.1, 0.4, 0.01]

# Ki[0]: starting value of ki gain
# Ki[1]: ending value of ki gain
# Ki[2]: increasing step of ki gain
Ki = [0.1, 0.4, 0.01]

# opt_err_perc: controls the percentage of the acceptable deviance from magnetic field of reference
opt_err_perc = 0.05

# stability_perc_thresh: controls the percentage that determines if the system is stable or not - for lower
#                        value of this percentage the code characterizes the system as unstable for lesser time
#                        above error goal
stability_perc_thresh = 0.05
