#include <Arduino.h>
#include <Wire.h>      
#include <BH1750.h>    

const int SWITCH_PIN = 2;      
const int LED_PIN = 3;        

// Switch Variables
volatile bool switchInterruptFlag = false; 
volatile unsigned long lastSwitchToggleTime = 0; 
const unsigned long debounceDelay = 200; 

// Light Sensor Variables
BH1750 lightSensor;                        
const unsigned long LIGHT_READ_INTERVAL = 500; 
const float LIGHT_THRESHOLD_LOW = 50.0;   
const float LIGHT_THRESHOLD_HIGH = 100.0;  
unsigned long lastLightReadTime = 0;       
bool lightSensorStateIsDark = false;      

volatile bool ledState = false;

// Function Declarations
void switchISR();
void handleSwitchInput();
void readAndProcessLightLevel(); 

//==============================================================================

void setup() {

  Serial.begin(9600);
  Wire.begin();


  if (lightSensor.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println(F("BH1750 Initialized successfully."));
  } else {
    Serial.println(F("Error initializing BH1750 sensor!"));
  }

  pinMode(SWITCH_PIN, INPUT_PULLUP); 
  pinMode(LED_PIN, OUTPUT);

  // Attach switch interrupt after setting up pins
  attachInterrupt(digitalPinToInterrupt(SWITCH_PIN), switchISR, CHANGE);
  Serial.print("Switch interrupt attached to pin: ");
  Serial.println(SWITCH_PIN);

}

//==============================================================================

void loop() {
  unsigned long currentMillis = millis(); 

  handleSwitchInput();

  if (currentMillis - lastLightReadTime >= LIGHT_READ_INTERVAL) {
    readAndProcessLightLevel(); 
    lastLightReadTime = currentMillis; 
  }
}

//==============================================================================

void switchISR() {
  switchInterruptFlag = true;
}

// Function to handle switch press flag and debounce logic
void handleSwitchInput() {
  if (switchInterruptFlag) {
    switchInterruptFlag = false; 

    unsigned long currentMillis = millis();
    // Check if enough time has passed since the last registered toggle
    if (currentMillis - lastSwitchToggleTime >= debounceDelay) {

      ledState = !ledState;
      digitalWrite(LED_PIN, ledState);

      Serial.print(currentMillis); // Timestamp for debugging
      Serial.print(" ms: Switch event! LED toggled to ");
      Serial.println(ledState ? "ON" : "OFF");

      lastSwitchToggleTime = currentMillis;
    }
  }
}

// Function to read the light sensor and toggle LED based on thresholds
void readAndProcessLightLevel() {
  float lux = lightSensor.readLightLevel();

  // Serial.print("Light Level: ");
  // Serial.print(lux);
  // Serial.println(" lx");

  bool wasStateDark = lightSensorStateIsDark;
  bool currentlyDark = (lux < LIGHT_THRESHOLD_LOW);
  bool currentlyLight = (lux > LIGHT_THRESHOLD_HIGH);

  // Update state if crossing any threshold (from dark to light or light to dark)
  if ((currentlyDark && !wasStateDark) || (currentlyLight && wasStateDark)) {
    lightSensorStateIsDark = currentlyDark;
    
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
    
    Serial.print("Threshold crossed: ");
    Serial.println(lightSensorStateIsDark ? "Dark" : "Light");
    Serial.print("LED toggled via light sensor to: ");
    Serial.println(ledState ? "ON" : "OFF");
  }
}