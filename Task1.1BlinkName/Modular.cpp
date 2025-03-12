#include <Arduino.h>

// Function declarations
void dot();
void dash();
void blinkMorse(char letter);

// Define a structure to represent Morse code for a letter
struct MorseCode {
  char letter;      // The alphabet character
  const char* code; // Pointer to the morse code string (dots and dashes)
};

// Array containing Morse code representations for the entire alphabet
MorseCode morseTable[] = {
    {'A', ".-"},   {'B', "-..."}, {'C', "-.-."}, {'D', "-.."},  {'E', "."},    
    {'F', "..-."}, {'G', "--."},  {'H', "...."}, {'I', ".."},   {'J', ".---"},  
    {'K', "-.-"},  {'L', ".-.."}, {'M', "--"},   {'N', "-."},   {'O', "---"},   
    {'P', ".--."}, {'Q', "--.-"}, {'R', ".-."},  {'S', "..."},  {'T', "-"},     
    {'U', "..-"},  {'V', "...-"}, {'W', ".--"},  {'X', "-..-"}, {'Y', "-.--"},  
    {'Z', "--.."}
  };

// Initialize the built-in LED pin as an output
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Define the message to be transmitted in Morse code
  char message[] = "AHMAD"; 

  // Loop through each character in the message
  for (int i = 0; i < sizeof(message) - 1; i++) {
    // Convert the current character to Morse code and blink it
    blinkMorse(message[i]);
    // Pause between letters
    delay(2000); 
  }
}

//  Converts a character to Morse code and blinks an LED accordingly.
//  Searches through the morseTable to find the Morse code for the given letter.
//  When found, it iterates through the code and calls dot() for '.' and dash() for '-'.

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
