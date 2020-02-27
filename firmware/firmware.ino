<<<<<<< HEAD
//===== Imports =====//
#include <Wire.h>
#include <Adafruit_MCP4725.h>
=======
import board
import busio
import adafruit_mcp4725

// PSEU: Imports
>>>>>>> 846bcf3281d650882ffc64993bf3565c8379ef0c

//===== Pin Definitions =====//
//---  Analog read ---//
#define SMACurrentReadPin A0
#define SMAVoltageReadPin A1
#define fanReadPin A2
#define posSensorReadPin A3

//--- Analog write ---//
#define fanWritePin 6

//===== Hardware Definitions =====//
Adafruit_MCP4725 dac;

//===== Constants =====//
float highV = 30.0; // High voltage
float lowV = 5.00;   // Low voltage

float maxSMACurrent = 0.5;   // Maximum SMA current

#define debug false

//===== Variables =====//
float SMACurrent;
float SMAVoltage;
float gripperWidth;

//===== Setup =====//
void setup() {
  Serial.begin(9600);

  analogReference(EXTERNAL); // NEVER REMOVE THIS

//  dac.begin(0x60);
//  dac.setVoltage(0, false);

  // Phase-correct PWM of 31.250 kHz (prescale factor of 1)
//  TCCR0A = _BV(COM0A1) | _BV(COM0B1) | _BV(WGM00);
//  TCCR0B = _BV(CS00);

  set_fanSpeed(0);
}

//===== Functions =====//
float check_serial() {
  if(Serial.available() > 0) {
    char data = Serial.read();
//    char str[2];
//    str[0] = data;
//    str[1] = '\0';
    Serial.print(data);
  }
}

void send_serial(char cmd) {
  Serial.write(cmd);
}

void set_SMACurrent(float SMACurrent) {
  //--- Set SMACurrent with DAC intfc ---//

  if (SMACurrent <= maxSMACurrent && SMACurrent >= 0) {
    int bitVoltage = (SMACurrent/lowV)*4095;
    dac.setVoltage(bitVoltage, false);

    if (debug) {
      Serial.print("set SMA Current: ");
      Serial.println(SMACurrent);
    }
  }
  else {
    Serial.println("Error, current out of range");
  }
}

float get_SMACurrent() {
  int bitCurrent = analogRead(SMACurrentReadPin);
  float SMACurrent = bitCurrent*lowV/1024;

  if (debug) {
    Serial.print("get SMA Current: ");
    Serial.println(SMACurrent);
  }

  return SMACurrent;
}

float get_SMAVoltage() {
  int bitVoltage = analogRead(SMAVoltageReadPin);
  float SMAVoltage = 7.8*bitVoltage*lowV/1024;

  if (debug) {
    Serial.print("get SMA Voltage: ");
    Serial.println(SMAVoltage);
  }

  return SMAVoltage;
}

void set_fanSpeed(int fanSpeedPer) {
  //--- Set fan speed (percent) ---//
  // NOTE: Untested

  int bitFanSpeed = min(max(fanSpeedPer,0),100) * 2.55; // 0-255
  analogWrite(fanWritePin, bitFanSpeed);

  if (debug) {
    Serial.print("Fan: ");
    Serial.println(fanSpeedPer);
  }
}

int get_fanSpeed() {
  //--- Read fan speed (percent) ---//
  // NOTE: Untested

  int bitFanSpeed = analogRead(fanReadPin);
  int fanSpeedPer = bitFanSpeed*100/1024;
  return fanSpeedPer;
}

int read_posSensor() {
  float volts = analogRead(posSensorReadPin);
  float distance = 27.726*pow(volts, -1.2045);
  distance = min(max(distance,0),30);
  return volts;
}

void adj_delay(int del) {
  delay(del*32);
  delay(del*32);
  delay(del*32);
  delay(del*32);
  delay(del*32);
}

//===== Loop =====//
void loop() {
//  get_serialCmd();
//
//  set_SMACurrent(0.2);
//  SMAVoltage = get_SMAVoltage();
//
//  Serial.print("Resistance: ");
//  Serial.println(SMAVoltage/0.2);

  long sum = 0;
  for (int i=0; i<200; i++) {
    sum += read_posSensor();
    delay(18);
  }
  Serial.println(sum/200.);
  // PSEU: Listen for serial commands
  // PSEU: If command -> set setPoint

  // PSEU: Read analog pins

  // PSEU: Determine SMACurrent (via P-Loop)
  // PSEU: Determine SMAResistance
  // PSEU: Limit SMACurrent (based on SMAResistance

  // PSEU: set_SMACurrent(SMACurrent)

  // PSEU: Return data over serial


}
