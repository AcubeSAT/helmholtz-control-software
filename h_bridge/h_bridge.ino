#include <multi_channel_relay.h>
#include <Wire.h>

Multi_Channel_Relay relay1;
Multi_Channel_Relay relay2;
Multi_Channel_Relay relay3;


const int BUFFER_SIZE = 100;
char buf[BUFFER_SIZE];

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

Multi_Channel_Relay relay;
    
void set_sign(uint8_t value) {


    if((value & 0xF0) == 0x10){
      relay = relay1;
    }
    else if((value & 0xF0) == 0x20){
      relay = relay2;
    } 
    else if((value & 0xF0) == 0x30){
      relay = relay3; 
    }
    
    if((value & 0x0F) == 0x00){
      sign = -1;
    }
    else if((value & 0x0F) == 0x01){
      sign = 1;
    } 
    
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


uint8_t value = 0;

void loop() {
  while (!Serial.available());
  
  if(Serial.available()>0){
    value = Serial.read(); 
    Serial.println(value);
    set_sign(value);
    Serial.flush();
    value = 0;
  }


  
//  Serial.print(sign);
}
