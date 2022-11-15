import numpy as np
import helmholtz_constants
from scipy import constants

class coil_current_control:

    def __init__(self, axis, desired_magnetic_field):
        self.axis = axis
        self.current = 0
        self.length = helmholtz_constants.coils[axis]
        self.initial_magnetic_field = helmholtz_constants.initial_magnetic_field[axis]
        self.desired_magnetic_field = desired_magnetic_field

    def get_desired_magnetic_field(self):
        return self.desired_magnetic_field

    def set_desired_magnetic_field(self,desired_magnetic_field):
        self.desired_magnetic_field = desired_magnetic_field

    def set_current(self):
        """
            Calculates current based on the magnetic field user commands, if calculated current
            exceeds expected value an error is raised.

            Returns: the current that needs to be applied
        """
        self.gamma = helmholtz_constants.beta / self.length
        self.current = ((self.desired_magnetic_field - self.initial_magnetic_field) * 1e-6 * np.pi * self.length) / (
                2 * constants.mu_0 * helmholtz_constants.wire_turns) * (
                               (1 + self.gamma ** 2) * np.sqrt(2 + self.gamma ** 2)) / 2

        assert abs(self.current) <= helmholtz_constants.PSU_max_current, "Current above max value"

    def get_current(self):
        return self.current

    def del_current(self):
        del self.current


