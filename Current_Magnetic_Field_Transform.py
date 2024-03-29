# Basic Python libraries
import numpy as np
import math

import helmholtz_constants

def input_magnetic_field_output_current(magnetic_field, side_length):
    """
        This function calculates the magnetic field created by a single current value.

        :param magnetic_field: the magnetic field creating a magnetic field
        :param side_length: coil side length (assuming the coil is a perfect square)

        :return: the current that produces the magnetic field
    """

    # distance between a pair of coils
    distance = side_length * 0.545

    # geometrical parameter dependent on the shape of coils
    geo_param = (8 * (side_length ** 2)) / (((side_length ** 2) + (distance ** 2)) * math.sqrt(
        2 * (side_length ** 2) + (distance ** 2)))

    current = (np.pi * magnetic_field) / (helmholtz_constants.MAG_PERM_AIR * helmholtz_constants.wire_turns * geo_param)

    return current


def input_current_output_magnetic_field(current, side_length):
    """
        This function calculates the magnetic field created by a single current value.

        :param current: the current creating a magnetic field
        :param side_length: coil side length (assuming the coil is a perfect square)

        :return: the magnetic field created by the given current

    """

    # distance between a pair of coils
    distance = side_length * 0.545

    # geometrical parameter dependent on the shape of coils
    geo_param = (8 * (side_length ** 2)) / (((side_length ** 2) + (distance ** 2)) * math.sqrt(
        2 * (side_length ** 2) + (distance ** 2)))

    magnetic_field = (helmholtz_constants.MAG_PERM_AIR * helmholtz_constants.wire_turns * current * geo_param) / np.pi

    return magnetic_field
