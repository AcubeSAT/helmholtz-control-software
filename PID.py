import numpy as np
import helmholtz_constants


class PID:
    def __init__(self):
        self.K_p = 1
        self.K_d = 1
        self.K_i = 1
        self.B_reference = 1
        self.B_measured = 1
        self.errors = np.array([1, 1, 1])
        self.current = 1

    def set_initial_current(self, initial_current):
        """
                   Changes current value to calculated initial current based on the commanded magnetic field

                   Args:
                      initial_current: initial_current calculated from the desired magnetic field

                """
        self.current = initial_current

    def set_reference_magnetic_field(self, B_reference):
        """
           Sets the value of B_reference (magnetic field) to the value user commanded.

           Args:
               B_reference: magnetic field commanded by the user

        """

        self.B_reference = B_reference

    def set_measured_magnetic_field(self, B_measured):
        """
           Sets the value of B_measured (magnetic field) to the measured value by system's magnetometer.

           Args:
               B_reference: magnetic field commanded by the user

       """

        self.B_measured = B_measured

    def update_errors(self):
        """
           Updates the errors between measured and commanded magnetic field for the last 3 timesteps.
           Each time a new error is calculated for the current time step, while the other errors move
           a time step behind. The error at k-2 timestep is overwritten.

       """

        error = self.B_reference - self.B_measured
        self.errors[2] = self.errors[1]
        self.errors[1] = self.errors[0]
        self.errors[0] = error

    def calculate_current(self):
        """
           Calculates the current based on the PID controller found in "Helmholtz cage design and
           validation for nanosatellites HWIL testing" paper, in order to adjust the magnetic
           field and minimize the error between the commanded and measured magnetic field.

           Returns: The new value of the current that needs to be applied.
        """

        current = self.current + self.K_p * (self.errors[0] - self.errors[1]) + \
                  self.K_i * self.errors[0] + \
                  self.K_d * (self.errors[0] - 2 * self.errors[1] + self.errors[2])

        self.current = current
        assert abs(self.current) <= helmholtz_constants.PSU_max_current, "Current above max value"
        return self.current
