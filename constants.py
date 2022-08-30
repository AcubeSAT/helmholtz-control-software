import numpy as np

coils = {'x_coil': 1.75,
         'y_coil': 1.70,
         'z_coil': 1.65
         }

initial_magnetic_field = {'x_axis': 10 ** -7,
                          'y_axis': 6.4 * 10 ** -6,
                          'z_axis': 10 ** -7
                          }

axis_current = {'current_axis_x': 1,
                'current_axis_y': 1,
                'current_axis_z': 1
                }

PSU_ports = {'PSU_x': np.array(['/dev/ttyUSB0', 'CH1']),
             'PSU_y': np.array(['/dev/ttyUSB0', 'CH2']),
             'PSU_z': np.array(['/dev/ttyUSB0', 'CH2'])
             }

wire_turns = 50
beta = 0.5445
