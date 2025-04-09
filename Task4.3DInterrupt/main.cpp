#include <Arduino.h>
#include <AS_BH1750.h>
#include <Wire.h>

// Timer interrupt includes and configuration
#define TIMER_INTERRUPT_DEBUG 0
#define _TIMERINTERRUPT_LOGLEVEL_ 0
#define USING_TIMER_TC3 true // Only TC3 can be used for SAMD51
// Timer library includes
#include "SAMDTimerInterrupt.h"
#include "SAMD_ISR_Timer.h"
// Timer configuration and objects
#define HW_TIMER_INTERVAL_MS 10
#define SELECTED_TIMER TIMER_TC3
// Init selected SAMD timer
SAMDTimer ITimer(SELECTED_TIMER);
// Init SAMD_ISR_Timer
SAMD_ISR_Timer ISR_Timer;
#define TIMER_INTERVAL_1S 1000L

// Pin Definitions
const int SWITCH_PIN = 2;  
const int TRIGGER_PIN = 4; 
const int ECHO_PIN = 5;    
const int LED1_PIN = 3;    // LED controlled by switch
const int LED2_PIN = 6;    // LED controlled by light sensor
const int LED3_PIN = 7;    // LED controlled by timer

// Global Variables
volatile bool led1State = false;             
volatile unsigned long lastDebounceTime = 0; 
const unsigned long debounceDelay = 80;      

AS_BH1750 lightMeter;

void TimerHandler(void)
{
    ISR_Timer.run();
}

void blinkLED3()
{
    static bool led3State = false;
    led3State = !led3State;
    digitalWrite(LED3_PIN, led3State);
    Serial.println("LED3 toggled by timer");
}

// ISR for switch
void handleSwitch()
{
    unsigned long currentTime = millis();
    if ((currentTime - lastDebounceTime) > debounceDelay)
    {
        led1State = !led1State;
        digitalWrite(LED1_PIN, led1State);
        Serial.print("Button pressed. LED1 state: ");
        Serial.println(led1State ? "ON" : "OFF");
        lastDebounceTime = currentTime; 
    }
}

void setup()
{
    Serial.begin(115200);

    pinMode(SWITCH_PIN, INPUT_PULLUP);
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(LED1_PIN, OUTPUT);
    pinMode(LED2_PIN, OUTPUT);
    pinMode(LED3_PIN, OUTPUT);

    attachInterrupt(digitalPinToInterrupt(SWITCH_PIN), handleSwitch, FALLING);

    Wire.begin();
    if (!lightMeter.begin())
    {
        Serial.println("Error initializing BH1750 sensor");
    }
    else
    {
        Serial.println("BH1750 sensor initialized");
    }

    // Initialize the timer for LED3
    if (ITimer.attachInterruptInterval_MS(HW_TIMER_INTERVAL_MS, TimerHandler))
    {
        Serial.print("Starting ITimer OK, millis() = ");
        Serial.println(millis());
    }
    else
    {
        Serial.println("Can't set ITimer. Select another freq. or timer");
    }

    // Set timer to blink LED3 every second
    ISR_Timer.setInterval(TIMER_INTERVAL_1S, blinkLED3);
}

void loop()
{
    float lux = lightMeter.readLightLevel();
    if (lux > 300)
    {
        digitalWrite(LED2_PIN, HIGH);
        Serial.println("Light level over 300 lux. LED2 ON.");
    }
    else
    {
        digitalWrite(LED2_PIN, LOW);
    }

    static unsigned long lastUltrasonicCheck = 0;
    const unsigned long ultrasonicInterval = 800; // Check every 800ms

    if (millis() - lastUltrasonicCheck >= ultrasonicInterval)
    {
        lastUltrasonicCheck = millis();

        long duration;
        float distance;

        // Trigger the ultrasonic sensor
        digitalWrite(TRIGGER_PIN, LOW);
        delayMicroseconds(2);
        digitalWrite(TRIGGER_PIN, HIGH);
        delayMicroseconds(10);
        digitalWrite(TRIGGER_PIN, LOW);

        // Read the echo pin
        duration = pulseIn(ECHO_PIN, HIGH, 60000); 

        if (duration > 0)
        {
            distance = (duration * 0.034) / 2;

            if (distance < 20)
            {
                Serial.println("Object detected within 20cm!");
            }
        }
        else
        {
            Serial.println("No valid echo received. Check sensor orientation and connections.");
        }
    }

    delay(100); 
}
