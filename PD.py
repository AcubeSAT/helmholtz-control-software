import helmholtz_constants


class PD:
    def __init__(self, K_p, K_d, K_dd):
        self.K_p = K_p
        self.K_d = K_d
        self.K_dd = K_dd
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
        current_measured = current_measured
        if abs(current_measured) >= helmholtz_constants.PSU_max_current:
            if current_measured > 2.5:
                current_measured = 2.5
            elif current_measured < -2.5:
                current_measured = -2.5
        self.current_measured = current_measured

    def get_measured_current(self):
        return self.current_measured

    def update_errors(self):
        self.error_2 = self.error_1
        self.error_1 = self.error_0
        self.error_0 = self.mf_desired - self.mf_measured

    def calculate_mf(self):

        self.mf_control = self.mf_control + self.K_p * self.error_0 + self.K_d * (self.error_0 - self.error_1) + self.K_dd * (self.error_0 - 2 * self.error_1 + self.error_2)

    def get_mf_control(self):
        return self.mf_control

