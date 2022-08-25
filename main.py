import PSU
import time

voltage_wanted = [1.0000, 1.1987, 1.3894, 1.5646, 1.7174, 1.8415, 1.9320, 1.9854, 1.9996, 1.9738, 1.9093, 1.8085,
                  1.6755, 1.5155, 1.3350, 1.1411, 0.9416, 0.7445, 0.5575, 0.3881, 0.2432, 0.1284, 0.0484, 0.0063,
                  0.0038, 0.0411, 0.1165, 0.2272, 0.3687, 0.5354, 0.7206, 0.9169, 1.0000]

frequency = 0.1 # in Hz (maximum 0.15 Hz)

time_to_sleep = 1/(frequency*len(voltage_wanted))

if __name__ == "__main__":
    trofodotiko = PSU()
    device = PSU(model='SPD3303C')

    current_values = [0, 0.2, 0.4, 0.6, 0.8, 1]
    volts_values = [0, 2, 4, 6, 8, 10]
    while 1:
        for voltage in voltage_wanted:
            trofodotiko.set_voltage_and_current(voltage, 0.1)
            time.sleep(time_to_sleep)

        for current_value, volts_value in zip(current_values, volts_values):
            device.set_channel(channel='CH1')
            device.set_current(current=current_value)
            time.sleep(0.1)
            device.set_voltage(voltage=volts_value)
            time.sleep(0.5)
            device.set_channel(channel='CH2')
            device.set_current(current=current_value)
            time.sleep(0.1)
            device.set_voltage(voltage=volts_value)
            time.sleep(0.5)
            print(device.measure_value('voltage'))
            print(device.measure_value('current'))
