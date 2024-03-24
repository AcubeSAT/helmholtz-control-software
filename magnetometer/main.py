import time
from magnetometer import Magnetometer

def main():
    # Initialize the magnetometer;
    mag = Magnetometer(port='/dev/ttyACM0')

    try:
        while True:
            magnetic_field = mag.get_magnetic_field()
            print(f"Magnetic field (X, Y, Z): {magnetic_field}")
            #time.sleep(1)  # Pause for a second
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()
