/*
This arduino code uses Adafruit_SensorLab in order to communicate
with the magnetometer
*/

#include <Adafruit_SensorLab.h>

#include <Adafruit_Sensor_Calibration.h>

Adafruit_SensorLab lab;

Adafruit_Sensor *mag = NULL;
sensors_event_t mag_event;

int loopcount = 0;

void setup(void) {
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Sensor Lab - IMU Calibration!"));
  lab.begin();

  Serial.println("Looking for a magnetometer");
  mag = lab.getMagnetometer();
  if (!mag) {
    Serial.println(F("Could not find a magnetometer, skipping!"));
  } else {
    mag->printSensorDetails();
  }
}

void loop() {
  if (mag && !mag->getEvent(&mag_event)) {
    return;
  }

  // we use the minus sign due to the alignment of the magnetometer with the helmholtz cage
//  Serial.print(-mag_event.magnetic.x); Serial.print(" ");
//  Serial.print(mag_event.magnetic.y); Serial.print(" ");
//  Serial.print(-mag_event.magnetic.z); Serial.println("");
  Serial.print(mag_event.magnetic.x); Serial.print(" ");
  Serial.print(mag_event.magnetic.y); Serial.print(" ");
  Serial.print(mag_event.magnetic.z); Serial.println("");

}
