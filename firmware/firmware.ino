import board
import busio
 
import adafruit_mcp4725

// PSEU: Imports

int SMACurrentPin = A0;
int SMAVoltagePin = A1;
int tachometerPin = A2;
int posSensorPin = A3;

i2c = busio.I2C(board.SCL, board.SDA)

// PSEU: Pin definitions

// set it up as an outcome function
dac = adafruit_mcp4725.MCP4725(i2c)
  
 
void setup() {
  Serial.begin(9600);
}

void set_SMACurrent(SMACurrent) {
  // PSEU: Send SMACurrent to DAC
}

void loop() {
  // PSEU: Listen for serial commands
  // PSEU: If command -> set setPoint
  
  // PSEU: Read analog pins
  
  // PSEU: Determine SMACurrent (via P-Loop)
  // PSEU: Determine SMAResistance
  // PSEU: Limit SMACurrent (based on SMAResistance
  
  // PSEU: set_SMACurrent(SMACurrent)

  // PSEU: Return data over serial
}
