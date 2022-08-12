from PSU import PSU
import numpy as np
import math

coils = {'x_coil': 1.75,
         'y_coil': 1.70,
         'z_coil': 1.65
         }

initial_magnetic_field = {'x_axis': 10 ** -7,
                          'y_axis': 10 ** -7,
                          'z_axis': 10 ** -7
                          }

wire_turns = 50
free_space_permeability = 1.2566 * 10 ** (-6)
beta = 0.5445


# def initial_state():
    # to be changed, get initial field measurements from magnetometer

    # initial_magnetic_field = { 'x_axis' : 10**-7,
    #                            'y_axis': 10 ** -7,
    #                             'z_axis' : 10**-7
    #                            }

def calculate_current(magnetic_field_commanded, axis):

    # initial_state()

    if axis == 'x' :
        length = coils['x_coil']
        initial_field = initial_magnetic_field['x_axis']
    elif axis == 'y':
        length = coils['y_coil']
        initial_field = initial_magnetic_field['y_axis']
    elif axis == 'z':
        length = coils['z_coil']
        initial_field = initial_magnetic_field['z_axis']
    else:
        return 0

    current = ((magnetic_field_commanded - initial_field)*np.pi*length)/(2*free_space_permeability*wire_turns)*((1+beta**2)*np.sqrt(2+beta**2))/2

    return current


print(calculate_current(-4*10**(-7),'y'))