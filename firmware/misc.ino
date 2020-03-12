#include "variables.h"

void calibrate() {
    get_SMACurrent();
    get_SMAVoltage();
    get_SMAResistance();

    while (SMAResistance <= maxResistance) {
        get_SMACurrent();
        get_SMAVoltage();
        get_SMAResistance();
        
        set_SMACurrent(SMACurrent + (maxResistance-SMAResistance)*Kp);
    }
    set_SMACurrent(0);
    float minPos = get_gripperWidth();

    return minPos;
}

float return_rawGripperWidth() {
  float volts = analogRead(posSensorReadPin);
  return volts;
}

unsigned long return_processorTime() {
  unsigned long t = millis();
  return t;
}

void adj_delay(int del) {
  delay(del*32);
  delay(del*32);
  delay(del*32);
  delay(del*32);
  delay(del*32);
}
