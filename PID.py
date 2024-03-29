import numpy as np
import helmholtz_constants


class PID:
    def __init__(self):
        self.K_p = 0
        self.K_d = 0
        self.K_i = 0
        self.errors = np.array([0, 0, 0])
        self.current_reference = 0
        self.current_measured = 0

    def set_reference_current(self, current_reference):
        """
           Sets the value of current_reference to the desired value, after transformation of the desired magnetic field to current.

           Args:
               current_reference: current_reference commanded
        """
        self.current_reference = current_reference

    def get_reference_current(self):
        return self.current_reference

    def set_measured_current(self, current_measured):
        """
           Sets the value of current_measured to the measured value, after transformation of the value of by system's magnetometer to current.

           Args:
               current_measured: current_measured 
       """
        self.current_measured = current_measured

    def get_measured_current(self):
        return self.measured_current

    def update_errors(self):
        """
            Updates the errors between measured and commanded magnetic field for the last 3 timesteps.
            Each time a new error is calculated for the current time step, the other errors move
            a time step behind. The error at k-2 timestep is overwritten.
        """
        self.errors[2] = self.errors[1]
        self.errors[1] = self.errors[0]
        self.errors[0] = self.current_reference - self.current_measured

    def calculate_current(self):
        """
           Calculates the current based on the PID controller found in "Helmholtz cage design and
           validation for nanosatellites HIL testing" paper, in order to adjust the magnetic
           field and minimize the error between the commanded and measured magnetic field.

           Returns: The new value of the current that needs to be applied.
        """

        self.current = self.current + self.K_p * (self.errors[0] - self.errors[1]) + \
                  self.K_i * self.errors[0] + \
                  self.K_d * (self.errors[0] - 2 * self.errors[1] + self.errors[2])


        assert abs(self.current) <= helmholtz_constants.PSU_max_current, "Current above max value"


    def get_current(self):
        return self.current
