
// Timer output	Arduino output	Chip pin	Pin name
// OC0A	        6	             12	        PD6

// Setting                          Prescale_factor
// TCCR0B = _BV(CS00);              1
// TCCR0B = _BV(CS01);              8
// TCCR0B = _BV(CS00) | _BV(CS01);  64
// TCCR0B = _BV(CS02);              256
// TCCR0B = _BV(CS00) | _BV(CS02);  1024
// PWM_frequency = (16 000 000)/(Prescale_factor*256);

// NOTE: I messed up by putting the output on Timer 0, this WILL affect delay() and milis()

//int fanPin = 6;
//
//void setup() {
//  Serial.begin(9600);
//
//  pinMode(fanPin, OUTPUT);  // sets the pin as output
//
//  // Phase-correct PWM of 31.250 kHz (prescale factor of 1)
//  TCCR0A = _BV(COM0A1) | _BV(COM0B1) | _BV(WGM00);
//  TCCR0B = _BV(CS00);
//}
//
//void loop() {
//  val = 0;
//  while (val < 255) {
//    val++;
//    analogWrite(fanPin, val); // Values 0 - 255
//  }
//  while (val > 0) {
//    val--;
//    analogWrite(fanPin, val); // Values 0 - 255
//  }
//}
