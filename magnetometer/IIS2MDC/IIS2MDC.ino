#include <IIS2MDCSensor.h>

#define SerialPort  Serial

#define IIS2MDC_I2C_SCL     PH4
#define IIS2MDC_I2C_SDA     PH5

TwoWire dev_i2c(IIS2MDC_I2C_SDA, IIS2MDC_I2C_SCL);

IIS2MDCSensor magnetometer(&dev_i2c);

void setup() {
  // Initialize serial for output
  SerialPort.begin(9600);

  // Initialize bus interface
  dev_i2c.begin();

  // Initlialize component
  magnetometer.begin();
  magnetometer.Enable();
}

void loop() {
  // Read magnetometer
  int32_t magnetic_field[3];
  magnetometer.GetAxes(magnetic_field);

  SerialPort.print("Mag[mGauss]:");
  Serial.print(magnetic_field[0]);
  Serial.print(", ");
  Serial.print(magnetic_field[1]);
  Serial.print(", ");
  Serial.println(magnetic_field[2]);
}
