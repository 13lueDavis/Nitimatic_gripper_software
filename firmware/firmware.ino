//===== Imports =====//
#include <Wire.h>
#include <Adafruit_MCP4725.h>
#include "RunningAverage.h"

//===== Hardware Definitions =====//
Adafruit_MCP4725 dac;

#include "variables.h"

String incomingString;
char command;
int payload;

//===== Setup =====//
void setup() {
  Serial.begin(9600);

  analogReference(EXTERNAL); // NEVER REMOVE THIS

  dac.begin(0x60);
  delay(100);
  dac.setVoltage(0, false);
  
  // Phase-correct PWM of 31.250 kHz (prescale factor of 1)
//  TCCR1A = _BV(COM0A1) | _BV(COM0B1) | _BV(WGM00);
//  TCCR1B = _BV(CS00);

  set_fanSpeed(50);
}

//===== Functions =====//
float check_serial() {
  if(Serial.available() > 0) {
    incomingString = Serial.readStringUntil('\r');
    command = incomingString.charAt(0);
    incomingString.remove(0,1);
    payload = incomingString.toInt();
    switch (command) {
        case 'm':
            set_calibrationM(float(payload)/1000);
            break;
        case 'b':
            set_calibrationB(float(payload)/1000);
            break;
        case 't':
            return_processorTime();
            break;
        case 'W':
            return_gripperWidth();
            break;
        case 'w':
            return_rawGripperWidth();
            break;
        case 'H':
            return_wireHealth();
            break;
        case 'i':
            set_targetCurrent(float(payload)/1000);
            break;
        case 'I':
            return_SMACurrent();
            break;
        case 'V':
            return_SMAVoltage();
            break;
        case 'R':
            return_SMAResistance();
            break;
        case 'c':
            break;
        case 'o':
            break;
        case 'f':
            set_fanSpeed(int(payload));
            break;
        case '+':
            return_info();
            break;
    }
  }
}

float return_SMACurrent() {
    Serial.println(SMACurrent);
    return SMACurrent;
}
float return_SMAVoltage() {
    Serial.println(SMAVoltage);
    return SMAVoltage;
}
float return_SMAResistance() {
    Serial.println(SMAResistance);
    return SMAResistance;
}
float return_gripperWidth() {
    Serial.println("111");
    return gripperWidth.getAverage();
}
int return_wireHealth() {
    Serial.println(wireHealth);
    return wireHealth;
}
void return_info() {
    Serial.print(SMACurrent);
    Serial.print(',');
    Serial.print(SMAVoltage);
    Serial.print(',');
    Serial.print(SMAResistance);
    Serial.print(',');
    Serial.print(gripperWidth.getAverage());
    Serial.print(',');
    Serial.print(wireHealth);
    Serial.print(',');
    Serial.println(millis());
}

//===== Loop =====//
void loop() {
    get_SMACurrent();
    get_SMAVoltage();
    get_SMAResistance();
    get_gripperWidth();

    return_info();
    
    check_serial();
    set_SMACurrent(targetCurrent);
}
