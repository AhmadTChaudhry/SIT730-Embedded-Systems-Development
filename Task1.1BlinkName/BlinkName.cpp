#include <Arduino.h>

// function declarations
void dot();
void dash();

void setup() {
  // setting up the LED pin as output
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // main code to flash AHMAD in morse code
  dot(); dash(); // A
  delay(2000);
  dot(); dot(); dot(); dot(); // H
  delay(2000);
  dash(); dash(); // M
  delay(2000); 
  dot(); dash(); // A
  delay(2000);
  dash(); dot(); dot(); // D
  delay(2000);
}

// function to blink LED as a dot for 300ms
void dot() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}

// function to blink LED as a dash for 900ms
void dash() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(900);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}