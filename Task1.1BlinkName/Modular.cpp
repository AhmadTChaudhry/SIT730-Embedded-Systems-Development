#include <Arduino.h>

// Function declarations
void dot();
void dash();
void blinkMorse(char letter);

struct MorseCode {
  char letter;
  const char* code;
};

MorseCode morseTable[] = {
    {'A', ".-"},   {'B', "-..."}, {'C', "-.-."}, {'D', "-.."},  {'E', "."},    
    {'F', "..-."}, {'G', "--."},  {'H', "...."}, {'I', ".."},   {'J', ".---"},  
    {'K', "-.-"},  {'L', ".-.."}, {'M', "--"},   {'N', "-."},   {'O', "---"},   
    {'P', ".--."}, {'Q', "--.-"}, {'R', ".-."},  {'S', "..."},  {'T', "-"},     
    {'U', "..-"},  {'V', "...-"}, {'W', ".--"},  {'X', "-..-"}, {'Y', "-.--"},  
    {'Z', "--.."}
  };

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  char message[] = "AHMAD"; 

  for (int i = 0; i < sizeof(message) - 1; i++) {
    blinkMorse(message[i]);
    delay(2000); 
  }
}

void blinkMorse(char letter) {
  for (MorseCode m : morseTable) {
    if (m.letter == letter) {
      for (int i = 0; m.code[i] != '\0'; i++) {
        if (m.code[i] == '.') {
          dot();
        } else if (m.code[i] == '-') {
          dash();
        }
      }
      return;
    }
  }
}

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
