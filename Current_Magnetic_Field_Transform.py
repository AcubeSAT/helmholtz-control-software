# Basic Python libraries
import numpy as np
import math

from scipy import constants
import helmholtz_constants

def input_magnetic_field_output_current(magnetic_field_control, side_length):
    """
        This function calculates the magnetic field created by a single current value.

        :param magnetic_field: the magnetic field creating a magnetic field
        :param side_length: coil side length (assuming the coil is a perfect square)

        :return: the current that produces the magnetic field
    """
    D = 0.9

    g = 8 * side_length**2 / ((side_length**2 + D**2) * np.sqrt(2*side_length**2 + D**2))

    current = (magnetic_field_control * np.pi) / (constants.mu_0 * helmholtz_constants.wire_turns * g)
    
    return current
