import numpy as np
import time

import helmholtz_constants
from PID import PID
from PSU import PSU
from coil_current_control import coil_current_control
from helmholtz_constants import initial_magnetic_field
from magnetometer import magnetometer
from h_bridge import sent_sign


def get_desired_magnetic_field():
    print('Command desired magnetic field for each axis in uT: ')
    desired_magnetic_field_uT_x, desired_magnetic_field_uT_y, desired_magnetic_field_uT_z = map(float, input().split())
    return np.array([desired_magnetic_field_uT_x * 10 ** -6, desired_magnetic_field_uT_y * 10 ** -6,
                     desired_magnetic_field_uT_z * 10 ** -6])


def get_initial_magnetic_field(magnetometer):
    for i in range(5):
        initial_field = magnetometer.get_magnetic_field()
    return initial_field


if __name__ == "__main__":

    desired_magnetic_field = get_desired_magnetic_field()
    II2MDC = magnetometer.Magnetometer()
    # loop to get the correct magnetometer values
    for _ in range(3):
        II2MDC.get_magnetic_field()

    SPD3303C = PSU('CH2', 'SPD3303C')
    time.sleep(.5)
    DP712 = PSU("CH1", 'DP712')

    helmholtz_constants.initial_magnetic_field['x'], helmholtz_constants.initial_magnetic_field['y'],helmholtz_constants.initial_magnetic_field['z'] = get_initial_magnetic_field(magnetometer=II2MDC)
    print(helmholtz_constants.initial_magnetic_field)
    # desired_magnetic_field =[1,1,1]
    coils = np.array(
        [
            coil_current_control('x', initial_magnetic_field['x']),
            coil_current_control('y', initial_magnetic_field['y']),
            coil_current_control('z', initial_magnetic_field['z'])])

    PID = [PID(), PID(), PID()]


    for i in range(3):
        coils[i].set_current()
        PID[i].set_initial_current(coils[i].get_current())

        if coils[i].axis == 'y':
            SPD3303C.set_channel('CH1')
            time.sleep(0.2)
            SPD3303C.set_current(0)
            time.sleep(0.2)
            SPD3303C.set_voltage(30)
            time.sleep(0.2)
        elif coils[i].axis == 'z':
            SPD3303C.set_channel('CH2')
            time.sleep(0.2)
            SPD3303C.set_current(0)
            time.sleep(0.2)
            SPD3303C.set_voltage(30)
            time.sleep(.2)
        else:
            time.sleep(.2)
            DP712.set_current(0)
            time.sleep(.2)
            DP712.set_voltage(30)
            time.sleep(.2)

        PID[i].set_initial_current(coils[i].get_current())
        PID[i].set_reference_magnetic_field(desired_magnetic_field[i])

# Open files for writing
    with open("magnetic_field_x_values.txt", "w") as file_x, \
         open("magnetic_field_y_values.txt", "w") as file_y, \
         open("magnetic_field_z_values.txt", "w") as file_z, \
         open("magnetic_field_all_values.txt", "w") as file_all, \
         open("noise_calculation_x.txt", "w") as noise_data_x, \
         open("noise_calculation_y.txt", "w") as noise_data_y, \
         open("noise_calculation_z.txt", "w") as noise_data_z, \
         open("noise_calculation_norm.txt", "w") as noise_data_norm : 
        while 1:
            for i in range(3):
                time.sleep(0.1)
                coils[i].set_desired_magnetic_field(desired_magnetic_field[i])
                coils[i].set_current()
                if coils[i].axis == 'y':
                    SPD3303C.set_channel('CH1')
                    time.sleep(0.1)
                    SPD3303C.set_current(abs(coils[i].get_current()))
                    time.sleep(0.1)
                    if coils[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.y_sign['negative'])
                    elif coils[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.y_sign['positive'])
                elif coils[i].axis == 'z':
                    SPD3303C.set_channel('CH2')
                    time.sleep(0.1)
                    SPD3303C.set_current(abs(coils[i].get_current()))
                    time.sleep(0.1)
                    if coils[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.z_sign['positive'])
                    elif coils[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.z_sign['negative'])
                else:
                    time.sleep(1)
                    DP712.set_current(abs(coils[i].get_current()))
                    time.sleep(0.2)
                    if coils[i].get_current() >= 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['negative'])
                    elif coils[i].get_current() < 0:
                        sent_sign.sent_sign(helmholtz_constants.x_sign['positive'])    
            
            # Calculate the theoretical field created by the helmholtz cage for each axis and the norm
            th = np.array([])
            for i in range(3):
                th[i] = coils[i].get_current() / (1e-6 * np.pi * self.length / (
                    2 * constants.mu_0 * helmholtz_constants.wire_turns) * (
                               (1 + self.gamma ** 2) * np.sqrt(2 + self.gamma ** 2)) / 2)
            th_norm = np.sqrt(th[0] ** 2 + th[1] ** 2 + th[2] ** 2)    
        #
            while 1:
                # print(SPD3303C.measure_current())
                # time.sleep(0.1)
                # print(DP712.measure_current())
                # time.sleep(.1)
                mf = II2MDC.get_magnetic_field()
                norm = np.sqrt(mf[0] ** 2 + mf[1] ** 2 + mf[2] ** 2)
                print(II2MDC.get_magnetic_field(), " ", norm)
                # Write values to respective files
                file_x.write(f"{mf[0]}\n")
                file_y.write(f"{mf[1]}\n")
                file_z.write(f"{mf[2]}\n")
                file_all.write(f"{mf[0]}, {mf[1]}, {mf[2]}\n")
                for f in [file_x, file_y, file_z, file_all]:
                    f.flush()  # Flush the buffer to ensure data is written immediately
                time.sleep(.1)
            
                # Calculate noise in each axis and the norm
                noise_x = mf[0] - initial_magnetic_field['x'] - th[0] 
                noise_y = mf[1] - initial_magnetic_field['y'] - th[1] 
                noise_z = mf[2] - initial_magnetic_field['z'] - th[2] 
                noise_norm =  np.sqrt(noise_x ** 2 + noise_y ** 2 + noise_z** 2)

                # Get the norm of the initial field
                initial_norm = np.sqrt(initial_magnetic_field['x'] ** 2 + initial_magnetic_field['y'] ** 2 + initial_magnetic_field['z'] ** 2)

                #write values to txt
                noise_data_x.write(f"{noise_x} {mf[0]} {initial_magnetic_field['x']} {th[0]} ")
                noise_data_y.write(f"{noise_y} {mf[1]} {initial_magnetic_field['y']} {th[1]} ")
                noise_data_z.write(f"{noise_z} {mf[2]} {initial_magnetic_field['z']} {th[2]} ")
                noise_data_norm.write(f"{noise_norm} {norm} {initial_norm} {th_norm} ")
                for f in [noise_data_x, noise_data_y, noise_data_z, noise_data_norm]:
                    f.flush()  # Flush the buffer to ensure data is written immediately
                time.sleep(.1)

    # while 1:
    #     # TODO: get measurements from magnetometer
    #     for i in range(2):
    #         PID[i].set_measured_magnetic_field(.01)
    #         PID[i].calculate_current()
    #
    #         if coils[i].axis == 'y':
    #             SPD3303C.set_channel('CH1')
    #             SPD3303C.set_current(0)
    #             SPD3303C.set_voltage(30)
    #         elif coils[i].axis == 'z':
    #             SPD3303C.set_channel('CH2')
    #             SPD3303C.set_current(0)
    #             SPD3303C.set_voltage(30)

    
