#include <ArduinoBLE.h>

const int trigPin = 4;
const int echoPin = 5;

// BLE Service and Characteristic UUIDs
BLEService parkingService("180C");
BLEByteCharacteristic distanceLevelChar("2A56", BLERead | BLENotify);

// Variables for change detection
uint8_t previousLevel = 255;
unsigned long lastUpdateTime = 0;
const unsigned long minUpdateInterval = 200;

void setup()
{
  Serial.begin(9600);
  while (!Serial && millis() < 5000)
    ;

  Serial.println("Starting Parking Sensor...");

  // Setup ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initialize BLE
  if (!BLE.begin())
  {
    Serial.println("Starting BLE failed!");
    while (1)
    {
      delay(1000);
    }
  }
  // Set BLE properties with standard connection parameters
  BLE.setLocalName("Nano33");
  BLE.setAdvertisedService(parkingService);
  parkingService.addCharacteristic(distanceLevelChar);
  BLE.addService(parkingService);
  distanceLevelChar.writeValue((uint8_t)0);
  // Start advertising
  BLE.advertise();
  Serial.println("BLE Parking Sensor Ready and Advertising...");
}

void loop()
{
  BLEDevice central = BLE.central();

  if (central)
  {
    Serial.print("Connected to RPi: ");
    Serial.println(central.address());

    while (central.connected())
    {
      unsigned long currentTime = millis();

      if (currentTime - lastUpdateTime >= minUpdateInterval)
      {
        long duration;
        int distance;

        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);

        duration = pulseIn(echoPin, HIGH, 30000);

        if (duration == 0)
        {
          Serial.println("No echo received (timeout)");
          delay(50);
          continue;
        }

        // Calculate distance in centimeters
        distance = duration * 0.034 / 2;

        // Determine level
        uint8_t level;
        if (distance < 10)
          level = 3;
        else if (distance < 20)
          level = 2;
        else if (distance < 30)
          level = 1;
        else
          level = 0;
        if (level != previousLevel || (currentTime - lastUpdateTime >= 500))
        {
          // Update BLE characteristic
          if (distanceLevelChar.writeValue(level))
          {
            previousLevel = level;
            lastUpdateTime = currentTime;
            Serial.print("Distance: ");
            Serial.print(distance);
            Serial.print(" cm | Level: ");
            Serial.println(level);
          }
          else
          {
            Serial.println("Failed to write characteristic value");
          }
        }
      }
      delay(50);
    }

    Serial.println("RPi disconnected");
  }
  delay(500);
}