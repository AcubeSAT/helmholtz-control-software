#include <IIS2MDCSensor.h>

#define SerialPort  Serial

#if defined(ARDUINO_B_U585I_IOT02A)
#define IIS2MDC_I2C_SCL     PC5
#define IIS2MDC_I2C_SDA     PC4                                                   
#else
// Uncomment to set I2C pins to use else default instance will be used
// #define IIS2MDC_I2C_SCL  PYn
// #define IIS2MDC_I2C_SDA  PYn
#endif
#if defined(IIS2MDC_I2C_SCL) && defined(IIS2MDC_I2C_SDA)
TwoWire dev_i2c(IIS2MDC_I2C_SDA, IIS2MDC_I2C_SCL);
#else
// X-NUCLEO-IKS02A1 uses default instance
#define dev_i2c       Wire
#endif

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

  SerialPort.print(magnetic_field[0]);
  Serial.print(" ");
  Serial.print(magnetic_field[1]);
  Serial.print(" ");
  Serial.println(magnetic_field[2]);
}
