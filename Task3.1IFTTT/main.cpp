#include <Wire.h>
#include <AS_BH1750.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>

// WiFi Credentials
const char *WIFI_SSID = "16 Pro";
const char *WIFI_PASSWORD = "12345678";

// Defining MQTT Credentials
#define MQTT_PASSWORD ":Ku6TGE#2,3do.xjC7hD"
#define MQTT_USER "hivemq.webclient.1742883968019"

#define MQTT_SERVER "dfbadadaa57f47fca9ecb74e0f5eeaac.s1.eu.hivemq.cloud"
#define MQTT_PORT 8883
#define MQTT_TOPIC_STATUS "terrarium/light/status"

AS_BH1750 lightSensor;
WiFiSSLClient wifiSSLClient;
PubSubClient mqttClient(wifiSSLClient);

// Configuration Parameters
const float SUNLIGHT_THRESHOLD_LUX = 350.0; // Minimum light level to detect sunlight
const unsigned long SEND_INTERVAL = 15000;  // Send data every 15 seconds

unsigned long lastSendTime = 0;
bool previousSunlightState = false;

// Function to connect to MQTT Broker
void connectMQTT()
{
  while (!mqttClient.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (mqttClient.connect("ArduinoNanoIoT", MQTT_USER, MQTT_PASSWORD))
    {
      Serial.println("Connected to MQTT Broker!");
      break;
    }
    else
    {
      Serial.print("Failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup()
{
  // Initializing Serial Monitor and Light Sensor
  Serial.begin(9600);
  delay(50);

  if (lightSensor.begin())
  {
    Serial.println("Light Sensor initialized successfully");
  }
  else
  {
    Serial.println("Light Sensor not detected");
    while(1);
  }

  // Initialize WiFi Connection
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  connectMQTT();
}

void loop()
{
  if (!mqttClient.connected()) {
    connectMQTT();
  }
  mqttClient.loop();

  unsigned long currentTime = millis();
  if (currentTime - lastSendTime >= SEND_INTERVAL)
  {
    float lightLevel = lightSensor.readLightLevel();
    bool isSunlightDetected = lightLevel >= SUNLIGHT_THRESHOLD_LUX;

    // Print Light Level to Serial Monitor
    Serial.print("Current Light Level: ");
    Serial.print(lightLevel);
    Serial.println(" lux");

    // Track sunlight Status Changes and Publish to MQTT
    if (isSunlightDetected && !previousSunlightState)
    {
      Serial.println("Sunlight Started");
      mqttClient.publish(MQTT_TOPIC_STATUS, "Sunlight Started");
    }
    else if (!isSunlightDetected && previousSunlightState)
    {
      Serial.println("Sunlight Ended");
      mqttClient.publish(MQTT_TOPIC_STATUS, "Sunlight Ended");
    }

    // Update Previous State
    previousSunlightState = isSunlightDetected;
    lastSendTime = currentTime;
  }
}