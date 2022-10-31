# H-bridge

## Contents
+ `h-bridge.ino` contains the code to be uploaded to an Arduino connected to the Relay Boards
+ `sent_sign.py` contains the code that achieves serial communication between a PC and the Arduino and sents to the Arduino the sign of the current that should flow each pair of coils  

## Dependencies
To use the scripts and functions of this folder, the [Multi_Channel_Relay_Arduino_Library](https://github.com/Seeed-Studio/Multi_Channel_Relay_Arduino_Library) is needed.

## Wiring
+ `Channel 1` <br>
  + `COM` -> VCC
  + `NO` -> one side of the coil
<br>
+ `Channel 2` <br>
  + `COM` -> one side of the coil
  + `NO` -> GND
<br>
+ `Channel 3` <br>
  + `COM` -> VCC
  + `NO` -> other side of the coil
<br>
+ `Channel 4` <br>
  + `COM` -> other side of the coil
  + `NO` -> GND