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

PSU_ports = {'x': np.array(['CH1', 'DP712']),
             'y': np.array(['CH2', 'SPD3303C']),
             'z': np.array(['CH2', 'SPD3303C'])
             }

wire_turns = 50
beta = 0.5445
