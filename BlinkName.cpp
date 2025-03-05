#include <Arduino.h>

// put function declarations here:
void dot();
void dash();

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
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

// put function definitions here:
void dot() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}

void dash() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(900);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}