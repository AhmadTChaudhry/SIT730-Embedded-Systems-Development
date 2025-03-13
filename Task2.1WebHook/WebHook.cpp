#include "DHT.h"
#include "secrets.h"
#include <WiFi.h>
#include <ThingSpeak.h>

#define DHTPIN 9      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22 // Setting DHT sensor type

DHT dht(DHTPIN, DHTTYPE);

// Defining safe temperature and humidity ranges
#define TEMP_MIN 10 // Minimum safe temperature (°C)
#define TEMP_MAX 30 // Maximum safe temperature (°C)

WiFiClient client;

void setup()
{
  Serial.begin(9600);
  Serial.println(F("DHT22 test with ThingSpeak!"));

  // Connect to WiFi
  WiFi.begin(SECRET_SSID, SECRET_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected!");

  // Initialize ThingSpeak
  ThingSpeak.begin(client);
  dht.begin();
}

void loop()
{
  // Wait between measurements
  delay(30000); // ThingSpeak needs minimum 15 seconds between updates

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Check if any reads failed and exit early
  if (isnan(h) || isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Print sensor data
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.println(F("°C"));

  // Alarm condition
  int alarmStatus = 0;
  if (t < TEMP_MIN || t > TEMP_MAX)
  {
    alarmStatus = 1; // Trigger alarm if values are out of range
    Serial.println("ALARM: Temperature Out of Range!");
  }

  // Set the fields with the values
  ThingSpeak.setField(1, t);
  ThingSpeak.setField(2, h);
  ThingSpeak.setField(3, alarmStatus);

  // Write ChannelID and API key to ThingSpeak channel
  int x = ThingSpeak.writeFields(SECRET_CH_ID, SECRET_WRITE_APIKEY);

  if (x == 200)
  {
    Serial.println("Channel update successful.");
  }
  else
  {
    Serial.println("Problem updating channel. HTTP error code " + String(x));
  }
}
