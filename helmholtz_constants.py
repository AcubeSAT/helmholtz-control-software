import numpy as np

coils = {'x': 1.75,
         'y': 1.70,
         'z': 1.65
         }

initial_magnetic_field = {'x': 10 ** -7,
                          'y': 6.4 * 10 ** -6,
                          'z': 10 ** -7
                          }

axis_current = {'x': 1,
                'y': 1,
                'z': 1
                }

PSU_ports = {'x': np.array(['/dev/ttyUSB0', 'CH1']),
             'y': np.array(['/dev/ttyUSB0', 'CH2']),
             'z': np.array(['/dev/ttyUSB0', 'CH2'])
             }

wire_turns = 50
beta = 0.5445
PSU_max_voltage = 30
PSU_max_current = 3