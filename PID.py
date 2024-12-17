# import numpy as np
# import helmholtz_constants


# class PID:
#     def __init__(self, K_p, K_d, K_i):
#         self.K_p = K_p
#         self.K_d = K_d
#         self.K_i = K_i
#         self.errors = np.array([0, 0, 0])
#         self.current_reference = 0
#         self.current_measured = 0

#     def set_reference_current(self, current_reference):
#         """
#            Sets the value of current_reference to the desired value, after transformation of the desired magnetic field to current.

#            Args:
#                current_reference: current_reference commanded
#         """
#         self.current_reference = current_reference

#     def get_reference_current(self):
#         return self.current_reference

#     def set_measured_current(self, current_measured):
#         """
#            Sets the value of current_measured to the measured value, after transformation of the value of by system's magnetometer to current.

#            Args:
#                current_measured: current_measured 
#        """
#         self.current_measured = current_measured

#     def get_current_measured(self):
#         return self.current_measured

#     def update_errors(self):
#         """
#             Updates the errors between measured and commanded magnetic field for the last 3 timesteps.
#             Each time a new error is calculated for the current time step, the other errors move
#             a time step behind. The error at k-2 timestep is overwritten.
#         """
#         self.errors[2] = self.errors[1]
#         self.errors[1] = self.errors[0]
#         self.errors[0] = self.current_reference - self.current_measured

#     def calculate_current(self):
#         """
#            Calculates the current based on the PID controller found in "Helmholtz cage design and
#            validation for nanosatellites HIL testing" paper, in order to adjust the magnetic
#            field and minimize the error between the commanded and measured magnetic field.

#            Returns: The new value of the current that needs to be applied.
#         """

#         self.current_measured = self.current_measured + self.K_p * (self.errors[0] - self.errors[1]) + \
#                   self.K_i * self.errors[0] + \
#                   self.K_d * (self.errors[0] - 2 * self.errors[1] + self.errors[2])
#         print(f"current is: {self.current_measured}")

#         if abs(self.current_measured) >= helmholtz_constants.PSU_max_current:
#             if self.current_measured > 0:
#                 self.current_measured = 2.5
#             elif self.current_measured < 0:
#                 self.current_measured = -2.5

#         # assert abs(self.current_measured) <= helmholtz_constants.PSU_max_current, "Current above max value"


import numpy as np
import helmholtz_constants


class PID:
    def __init__(self, K_p, K_d, K_dd):
        self.K_p = K_p
        self.K_d = K_d
        # self.K_i = K_i
        self.K_dd = K_dd
        # self.errors = np.array([0, 0, 0])
        self.error_0 = 0
        self.error_1 = 0
        self.error_2 = 0
        self.mf_desired = 0
        self.mf_measured = 0
        self.current_measured = 0
        self.mf_control = 0

    def set_desired_mf(self, mf_desired):
        self.mf_desired = mf_desired

    def get_desired_mf(self):
        return self.mf_desired

    def set_measured_mf(self, mf_measured):
        self.mf_measured = mf_measured

    def get_measured_mf(self):
        return self.mf_measured
    
    def set_measured_current(self, current_measured):
        if abs(current_measured) >= helmholtz_constants.PSU_max_current:
            print(f"Current is: {current_measured}")
            if current_measured > 2.5:
                current_measured = 2.5
            elif current_measured < -2.5:
                current_measured = -2.5
        # print(f"Current is: {self.current_measured}")
        self.current_measured = current_measured

    def get_measured_current(self):
        return self.current_measured

    def update_errors(self):
        # self.errors[2] = self.errors[1]
        # self.errors[1] = self.errors[0]
        # self.errors[0] = self.mf_measured - self.mf_desired
        self.error_2 = self.error_1
        self.error_1 = self.error_0
        self.error_0 = self.mf_measured - self.mf_desired
        # print(f"mf_measured: {self.mf_measured}")
        # print(f"mf_desired: {self.mf_desired}")
        # print(f"Error is: {self.mf_measured - self.mf_desired}")
        # print(f"Eimai sthn update 0: {self.error_0}")

    def calculate_mf(self):

        self.mf_control = self.K_p * self.error_0 + self.K_d * (self.error_0 - self.error_1) + self.K_dd * (self.error_0 - 2 * self.error_1 + self.error_2)

        # print(f"MF is: {self.mf_control}")
        # print(f"1 is: {self.K_p * self.error_0}")
        # print(f"2 is: {self.K_p * (self.error_0 - self.error_1)}")
        # print(f"3 is: {self.K_dd * (self.error_0 - 2 * self.error_1 + self.error_2)}")
        # print(f"0: {self.error_0}")
        # print(f"1: {self.error_1}")
        # print(f"2: {self.error_2}")
        # print(self.error_0 - self.error_1)
        # print(self.error_0 - 2 * self.error_1 + self.error_2)

    def get_mf_control(self):
        return self.mf_control

