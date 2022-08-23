import numpy as np


class PID:
    def __init__(self, K_p, K_d, K_i, B_reference, B_measured, errors, current):
        self.K_p = 1
        self.K_d = 1
        self.K_i = 1
        self.B_reference = 1
        self.B_measured = 1
        self.errors = np.array([1, 1, 1])
        self.current = 1

    """
       Sets the value of B_reference (magnetic field) to the value user commanded.

       Args:
           B_reference: magnetic field commanded by the user
           
    """

    def get_reference_magnetic_field(self, B_reference):
        self.B_reference = B_reference

    """
       Sets the value of B_measured (magnetic field) to the measured value by system's magnetometer.

       Args:
           B_reference: magnetic field commanded by the user

   """

    def get_measured_magnetic_field(self, B_measured):
        self.B_measured = B_measured

    """
       Updates the errors between measured and commanded magnetic field for the last 3 timesteps.
       Each time a new error is calculated for the current time step, while the other errors move
       a time step behind. The error at k-2 timestep is overwritten.

   """

    def update_errors(self):
        error = self.B_reference - self.B_measured
        self.errors[2] = self.errors[1]
        self.errors[1] = self.errors[0]
        self.errors[0] = error

    """
       Calculates the current based on the PID controller found in "Helmholtz cage design and 
       validation for nanosatellites HWIL testing" paper, in order to adjust the magnetic 
       field and minimize the error between the commanded and measured magnetic field.
    
       Returns: The new value of the current that needs to be applied.
    """

    def calculate_current(self):
        current = self.current + self.K_p * (self.errors[0] - self.errors[1]) + \
                  self.K_i * self.errors[0] + \
                  self.K_d * (self.errors[0] - 2 * self.errors[1] + self.errors[2])

        self.current = current

        return self.current
