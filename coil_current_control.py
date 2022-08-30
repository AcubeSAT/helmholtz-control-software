from PSU import PSU
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
        self.axis_PSU = PSU(helmholtz_constants.PSU_ports[axis][0], helmholtz_constants.PSU_ports[axis][1])

    def initialize_PSU(self):
        """
           Used to initialize the PSU that controls the axis at the start of the operation.
           Voltage is set to maximum (30V) and current is set to 0 in order to have
           the magnetic field in the Helmholtz Cage unaffected.

       """
        self.axis_PSU.set_voltage_and_current(helmholtz_constants.PSU_max_voltage, 0)

    def initial_current(self):
        """
            Calculates current based on the magnetic field user commands, if calculated current
            exceeds expected value an error is raised.

            Returns: the current that needs to be applied
        """

        self.current = ((self.desired_magnetic_field - self.initial_magnetic_field) * np.pi * self.length) / (
                2 * constants.mu_0 * helmholtz_constants.wire_turns) * (
                               (1 + helmholtz_constants.beta ** 2) * np.sqrt(2 + helmholtz_constants.beta ** 2)) / 2

        assert abs(self.current) <= helmholtz_constants.PSU_max_current, "Current above max value"

    def command_PSU_current(self):
        """
           Changes PSUs' current to commanded vlaue.
        """

        self.axis_PSU.set_current(abs(self.current))

