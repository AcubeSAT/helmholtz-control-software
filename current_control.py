from PSU import PSU
import numpy as np
from PID import PID

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
free_space_permeability = 1.2566 * 10 ** (-6)
beta = 0.5445

"""
    Calculates current based on the magnetic field user commands.  

    Args:
        commanded_magnetic_field: the magnetic field user wants to be applied
        axis: the axis the current is commanded

    Returns: the current that needs to be applied
    """


def calculate_current(commanded_magnetic_field, axis):
    if axis == 'x':
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

    current = ((commanded_magnetic_field - initial_field) * np.pi * length) / (
                2 * free_space_permeability * wire_turns) * ((1 + beta ** 2) * np.sqrt(2 + beta ** 2)) / 2

    return current


"""
    Used as a protection in order not to stress PSUs over their limit. If a current value greater 
    than 3A is commanded then the applied current is equal to 3A

    Args:
        calculated_current: the current that will be checked
        

    Returns: The applied current
    """


def overload_control(calculated_current):
    if calculated_current > 3:
        current = 3
    else:
        current = calculated_current

    return current


"""
   Description
   User can decide either to command the magnetic flux density of the whole homogeneous area (each axis 
   has the same magnetic field) or the magnetic field for each axis separately. Function changes the values
   in the axis_current dictionary

   Args:
       operation_mode: this argument has to values 0 and 1. 
       If operation_mode == 0, user can choose the norm of the magnetic field to be applied
       in the center of the coil. Each axis has the same magnetic field. 
       If operation_mode == 1, user can define the current for each axis separately.  
      
   """


# When operation_mode = 1 user can change magnetic field's rate, each axis produces the same magnetic field.
# When operation mode = 2 user can adjust the magnetic field in each axis individually
def mode(operation_mode):
    if operation_mode == 0:
        print("Choose magnetic field's density:")
        magnetic_field_density = float(input())
        axis_magnetic_field = (1 / np.sqrt(3)) * magnetic_field_density

        current = calculate_current(axis_magnetic_field, 'x')
        current = overload_control(current)
        axis_current['current_axis_x'] = current

        current = calculate_current(axis_magnetic_field, 'y')
        current = overload_control(current)
        axis_current['current_axis_y'] = current

        current = calculate_current(axis_magnetic_field, 'z')
        current = overload_control(current)
        axis_current['current_axis_z'] = current

    elif operation_mode == 1:

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

        magnetic_field_density = np.sqrt(
            magnetic_field_density_x ** 2 + magnetic_field_density_y ** 2 + magnetic_field_density_z ** 2)
        print(magnetic_field_density)


PSU_x = PSU(PSU_ports['PSU_x'][0], PSU_ports['PSU_x'][1])
PSU_y = PSU(PSU_ports['PSU_y'][0], PSU_ports['PSU_y'][1])
PSU_z = PSU(PSU_ports['PSU_z'][0], PSU_ports['PSU_z'][1])

"""
   Changes PSUs' current to commanded vlaue.

   Args:
       PSU: The power supply unit that has its current value changed
       current: the commanded current

   """


def command_PSU_current(PSU, current):
    PSU.set_current(current=current)


"""
   Used to initialize PSUs at the start of the operation. Voltage is set to maximum (30V) and
   current is set to 0 in order to have the magnetic field in the Helmholtz Cage unaffected.

   Args:
       PSU_(x,y,z): passes the PSU object for each axis (x,y,z) respectively

   """


def initialize_PSUs(PSU_x, PSU_y, PSU_z):
    PSU_x.set_voltage_and_current(30, 0)
    PSU_y.set_voltage_and_current(30, 0)
    PSU_z.set_voltage_and_current(30, 0)
