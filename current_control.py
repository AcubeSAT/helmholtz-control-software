from PSU import PSU
import numpy as np
from PID import PID

coils = {'x_coil': 1.75,
         'y_coil': 1.70,
         'z_coil': 1.65
         }

initial_magnetic_field = {'x_axis': 10 ** -7,
                          'y_axis': 6.4*10**-6,
                          'z_axis': 10 ** -7
                          }

axis_current = {'current_axis_x' : 1,
                'current_axis_y' : 1,
                'current_axis_z' : 1
                }

PSU_ports = {'DP712': ['/dev/ttyUSB0', 'CH1'],
             'SPD3303C_CH1': ['/dev/ttyUSB0', 'CH2'],
             'SPD3303C_CH2': ['/dev/ttyUSB0', 'CH2']
             }


wire_turns = 50
free_space_permeability = 1.2566 * 10 ** (-6)
beta = 0.5445



def calculate_current(commanded_magnetic_field, axis):

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

    current = ((commanded_magnetic_field - initial_field)*np.pi*length)/(2*free_space_permeability*wire_turns)*((1+beta**2)*np.sqrt(2+beta**2))/2

    return current

def overload_control(calculated_current):

    if calculated_current > 3:
        current = 3
    else:
        current = calculated_current
    return current

# When operation_mode = 1 user can change magnetic field's rate, each axis produces the same magnetic field.
# When operation mode = 2 user can adjust the magnetic field in each axis individually
def mode(operation_mode):

    if operation_mode == 1:
        print("Choose magnetic field's density:")
        magnetic_field_density = float(input())
        axis_magnetic_field = (1/np.sqrt(3))*magnetic_field_density

        current = calculate_current(axis_magnetic_field,'x')
        current = overload_control(current)
        axis_current['current_axis_x'] = current

        current = calculate_current(axis_magnetic_field, 'y')
        current = overload_control(current)
        axis_current['current_axis_y'] = current

        current = calculate_current(axis_magnetic_field, 'z')
        current = overload_control(current)
        axis_current['current_axis_z'] = current

    elif operation_mode == 2 :

        print("Choose magnetic field's density in x axis:")
        magnetic_field_density_x = float(input())

        current = calculate_current(magnetic_field_density_x, 'x')
        current = overload_control(current)
        axis_current['current_axis_x'] = current

        print("Choose magnetic field's density in y axis:")
        magnetic_field_density_y = float(input())
        current = calculate_current(magnetic_field_density_y, 'y')
        current = overload_control(current)
        axis_current['current_axis_y'] = current

        print("Choose magnetic field's density in z axis:")
        magnetic_field_density_z = float(input())
        current = calculate_current(magnetic_field_density_z, 'z')
        current = overload_control(current)
        axis_current['current_axis_z'] = current

        magnetic_field_density = np.sqrt(magnetic_field_density_x**2+magnetic_field_density_y**2+magnetic_field_density_z**2)
        print(magnetic_field_density)

voltage = 30

def command_PSU_current(PSU_name,current):

    PSU_used = PSU(PSU_ports[PSU_name][0],PSU_ports[PSU_name][1])
    PSU_used.set_current(current=current)

def initialize_PSUs():

    DP712 = PSU(PSU_ports['DP712'][0],PSU_ports['DP712'][1])
    SPD3303C_CH1 = PSU(PSU_ports['SPD3303C_CH1'][0],PSU_ports['SPD3303C_CH1'][1])
    SPD3303C_CH2 = PSU(PSU_ports['SPD3303C_CH2'][0], PSU_ports['SPD3303C_CH2'][1])

    DP712.set_voltage_and_current(30,0)
    SPD3303C_CH1.set_voltage_and_current(30,0)
    SPD3303C_CH2.set_voltage_and_current(30,0)



