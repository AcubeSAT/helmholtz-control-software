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

//  Serial.println("Looking for a gyroscope");
//  gyro = lab.getGyroscope();
//  if (!gyro) {
//    Serial.println(F("Could not find a gyroscope, skipping!"));
//  } else {
//    gyro->printSensorDetails();
//  }
//
//  Serial.println("Looking for an accelerometer");
//  accel = lab.getAccelerometer();
//  if (!accel) {
//    Serial.println(F("Could not find an accelerometer, skipping!"));
//  } else {
//    accel->printSensorDetails();
//  }
}

void loop() {
  if (mag && !mag->getEvent(&mag_event)) {
    return;
  }

  // 'Raw' values to match expectation of MOtionCal
//  Serial.print("Raw:");
//  Serial.print(int(accel_event.acceleration.x * 8192 / 9.8)); Serial.print(",");
//  Serial.print(int(accel_event.acceleration.y * 8192 / 9.8)); Serial.print(",");
//  Serial.print(int(accel_event.acceleration.z * 8192 / 9.8)); Serial.print(",");
//  Serial.print(int(gyro_event.gyro.x * Adafruit_SensorLab::DEGREES_PER_RADIAN * 16)); Serial.print(",");
//  Serial.print(int(gyro_event.gyro.y * Adafruit_SensorLab::DEGREES_PER_RADIAN * 16)); Serial.print(",");
//  Serial.print(int(gyro_event.gyro.z * Adafruit_SensorLab::DEGREES_PER_RADIAN * 16)); Serial.print(",");
//  Serial.print(int(mag_event.magnetic.x * 10)); Serial.print(",");
//  Serial.print(int(mag_event.magnetic.y * 10)); Serial.print(",");
//  Serial.print(int(mag_event.magnetic.z * 10)); Serial.println("");

  // unified data
//  Serial.print("Uni:");
//  Serial.print(accel_event.acceleration.x); Serial.print(",");
//  Serial.print(accel_event.acceleration.y); Serial.print(",");
//  Serial.print(accel_event.acceleration.z); Serial.print(",");
//  Serial.print(gyro_event.gyro.x, 4); Serial.print(",");
//  Serial.print(gyro_event.gyro.y, 4); Serial.print(",");
//  Serial.print(gyro_event.gyro.z, 4); Serial.print(",");
//  Serial.print(-(mag_event.magnetic.x-26)); Serial.print(" ");
//  Serial.print(mag_event.magnetic.y-9.5); Serial.print(" ");
//  Serial.print(-(mag_event.magnetic.z+49)); Serial.println("");
  Serial.print(mag_event.magnetic.x); Serial.print(" ");
  Serial.print(mag_event.magnetic.y); Serial.print(" ");
  Serial.print(mag_event.magnetic.z); Serial.println("");

//  Serial.end();
}
