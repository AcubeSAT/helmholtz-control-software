from PSU import PSU
import time

voltage_wanted = [1.0000, 1.1987, 1.3894, 1.5646, 1.7174, 1.8415, 1.9320, 1.9854, 1.9996, 1.9738, 1.9093, 1.8085,
                  1.6755, 1.5155, 1.3350, 1.1411, 0.9416, 0.7445, 0.5575, 0.3881, 0.2432, 0.1284, 0.0484, 0.0063,
                  0.0038, 0.0411, 0.1165, 0.2272, 0.3687, 0.5354, 0.7206, 0.9169, 1.0000]

frequency = 0.1 # in Hz (maximum 0.15 Hz)

time_to_sleep = 1/(frequency*len(voltage_wanted))

if __name__ == "__main__":
    trofodotiko = PSU()
    while 1:
        for voltage in voltage_wanted:
            trofodotiko.set_voltage_and_current(voltage, 0.1)
            time.sleep(time_to_sleep)
