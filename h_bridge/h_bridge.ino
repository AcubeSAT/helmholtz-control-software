#include <multi_channel_relay.h>
#include <Wire.h>

Multi_Channel_Relay relay1, relay2, relay3;

int sign;
int index;
void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
 
    relay1.begin(0x20);
    relay2.begin(0x21);
    relay3.begin(0x22);
    
  for(int i=1; i<=4; i++) {
    relay1.turn_off_channel(i);
    relay2.turn_off_channel(i);
    relay3.turn_off_channel(i);
  }
}

void set_sign(Multi_Channel_Relay relay) {

    
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
int value;

void loop() {
  while (Serial.available());

  sign = Serial.readString().toInt();
  
  if(sign == 100){
  set_sign(relay1);
  }
  else if (sign == 200){
  set_sign(relay2);
  } 
  else if (sign == 300){
    set_sign(relay3);
    }

  
//  Serial.print(sign);
}
