#ifndef VARIABLES
#define VARIABLES

//===== Pin Definitions =====//
//---  Analog read ---//
#define SMACurrentReadPin A6
#define SMAVoltageReadPin A0
#define fanReadPin A7
#define posSensorReadPin A1

//--- Analog write ---//
#define fanWritePin 9

//===== Constants =====//
const float highV = 30.0; // High voltage
const float lowV = 5.00;   // Low voltage

const int maxResistance = 38;
const int minResistance = 31;

const float maxSMACurrent = 0.5;   // Maximum SMA current

const float Kp = 0.01;

#define debug false

//===== Variables =====//
float SMACurrent = 0.0;
float SMAVoltage = 0.0;
float SMAResistance = 0.0;
RunningAverage gripperWidth(20);

float calibrationM = -2.777;  // From datasheet (run calibrate() from backend)
float calibrationB = 11.5677;

float targetCurrent = 0.3;

int wireHealth = 1;

#endif
