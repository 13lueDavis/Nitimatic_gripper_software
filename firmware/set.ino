#include "variables.h"

void set_targetCurrent(float setPoint) {
    targetCurrent = setPoint;
    return targetCurrent;
}

void set_SMACurrent(float desiredCurrent) {
  //--- Set SMACurrent with DAC intfc ---//

  if (desiredCurrent <= maxSMACurrent && desiredCurrent >= 0) {
    int bitVoltage = (desiredCurrent/lowV)*4095;
    dac.setVoltage(bitVoltage, false);
  }
}

void set_fanSpeed(int fanSpeedPer) {
  int bitFanSpeed = min(max(fanSpeedPer,0),100) * 2.55; // 0-255
  analogWrite(fanWritePin, bitFanSpeed);
  return fanSpeedPer;
}

void set_calibrationM(float m) {
  calibrationM = m;
  Serial.println('1');
}

void set_calibrationB(float b) {
  calibrationB = b;
  Serial.println('1');
}
