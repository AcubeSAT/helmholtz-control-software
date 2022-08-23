import numpy as np
class PID:
    def __init__(self, K_p, K_d,K_i, B_reference, B_measured, errors, current):
        self.K_p = 1
        self.K_d = 1
        self.K_i = 1
        self.B_reference = 1
        self.B_measured = 1
        self.errors = np.array([1, 1, 1])
        self.current = 1

    def get_reference_magnetic_field(self, B_reference):
        self.B_reference = B_reference

    def get_measured_magnetic_field(self, B_measured):
        self.B_measured = B_measured

    def update_errors(self):
        error = self.B_reference - self.B_measured
        self.errors[2] = self.errors[1]
        self.errors[1] = self.errors[0]
        self.errors[0] = error

    def calculate_current(self):
        current = self.current + self.K_p * (self.errors[0] - self.errors[1]) + \
                  self.K_i * self.errors[0] + \
                  self.K_d * (self.errors[0] - 2 * self.errors[1] + self.errors[2])

        self.current = current

        return self.current

