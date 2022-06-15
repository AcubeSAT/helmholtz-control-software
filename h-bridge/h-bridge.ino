#include <multi_channel_relay.h>

Multi_Channel_Relay relay;
int sign;

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
    relay.begin(0x11);

  for(int i=1; i<=4; i++) {
    relay.turn_off_channel(i);
  }
}

void set_sign() {
    if(sign < 0) {
        for(int i=1; i<=4; i++) {
            relay.turn_off_channel(i);
        }
        relay.turn_on_channel(2);
        relay.turn_on_channel(3);
    }

    if(sign > 0) {
        for(int i=1; i<=4; i++) {
            relay.turn_off_channel(i);
        }
            relay.turn_on_channel(4);
            relay.turn_on_channel(1);
    }
}

void loop() {
  while (!Serial.available());

  sign = Serial.readString().toInt();
  set_sign();

//  Serial.print(sign);
}