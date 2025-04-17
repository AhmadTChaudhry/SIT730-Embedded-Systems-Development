#include <Arduino.h>
#include <WiFiNINA.h>
#include <Firebase_Arduino_WiFiNINA.h>
#include <secrets.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 6
#define LED_COUNT 24

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
FirebaseData fbdo;

void setStripColor(uint32_t colorValue)
{
    strip.clear();
    for (int i = 0; i < LED_COUNT; i++)
    {
        strip.setPixelColor(i, colorValue);
    }
    strip.show();
}

bool getStateFromJson(const String &json, const String &color)
{
    String searchKey = "\"" + color + "\":{";
    int colorIndex = json.indexOf(searchKey);
    if (colorIndex == -1)
        return false;

    int stateIndex = json.indexOf("\"state\":", colorIndex);
    if (stateIndex == -1)
        return false;

    int valueStart = stateIndex + 8;              
    int valueEnd = json.indexOf(",", valueStart); 

    if (valueEnd == -1)
        valueEnd = json.indexOf("}", valueStart);

    if (valueEnd == -1)
        return false;

    String value = json.substring(valueStart, valueEnd);
    value.trim();

    return value == "true";
}

void setup()
{
    Serial.begin(9600);
    strip.begin();
    strip.show();
    strip.setBrightness(50);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");

    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH, WIFI_SSID, WIFI_PASSWORD);
    Firebase.reconnectWiFi(true);
    Serial.println("Connected to Firebase Traffic Light Database");
}

void loop()
{
    if (Firebase.getJSON(fbdo, "/trafficLights"))
    {
        String json = fbdo.jsonData();

        bool redState = getStateFromJson(json, "red");
        bool yellowState = getStateFromJson(json, "yellow");
        bool greenState = getStateFromJson(json, "green");

        uint32_t finalColor = 0;
        const char *colorName = "OFF";

        if (redState)
        {
            finalColor = strip.Color(255, 0, 0); // Red
            colorName = "RED";
        }
        else if (yellowState)
        {
            finalColor = strip.Color(255, 165, 0); // Yellow
            colorName = "YELLOW";
        }
        else if (greenState)
        {
            finalColor = strip.Color(0, 255, 0); // Green
            colorName = "GREEN";
        }

        Serial.print("Setting color to: ");
        Serial.println(colorName);
        setStripColor(finalColor);
    }
    else
    {
        Serial.print("Firebase.getJSON failed: ");
        Serial.println(fbdo.errorReason());
        setStripColor(0);
    }

    delay(500);
}
