#include "variables.h"

float get_SMACurrent() {
  int bitCurrent = analogRead(SMACurrentReadPin);
  SMACurrent = (bitCurrent*lowV/1024)/1.96;
  return SMACurrent;
}

float get_SMAVoltage() {
  int bitVoltage = analogRead(SMAVoltageReadPin);
  SMAVoltage = 7.8*bitVoltage*lowV/1024;
  return SMAVoltage;
}

float get_SMAResistance() {
    SMAResistance = SMAVoltage/SMACurrent;
}

int get_gripperHealth() {
    return 2;
}

int get_fanSpeed() {
  //--- Read fan speed (percent) ---//
  // NOTE: Untested

  int bitFanSpeed = analogRead(fanReadPin);
  int fanSpeedPer = bitFanSpeed*100/1024;
  return fanSpeedPer;
}

float get_gripperWidth() {
    // CHANGE TO BE A ROLLING AVERAGE
  float volts = analogRead(posSensorReadPin)*lowV/1024.;
  float dist = calibrationM*volts + calibrationB;
  gripperWidth.addValue(volts);
  return gripperWidth.getAverage();
}
