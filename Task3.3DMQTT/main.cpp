#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ESP_Mail_Client.h>
#include "arduino_secrets.h" 

// WiFi and Email Credentials
#define WIFI_SSID SECRET_SSID
#define WIFI_PASS SECRET_PASS
#define SMTP_HOST "smtp.gmail.com"
#define SMTP_PORT 465
#define AUTHOR_EMAIL SECRET_EMAIL_USERNAME
#define AUTHOR_PASSWORD SECRET_EMAIL_PASSWORD
#define RECIPIENT_EMAIL "s224227027@deakin.edu.au" 

// Pin Definitions
const int LED1 = 3;
const int LED2 = 6;
const int LED3 = 7;
const int TRIGGER_PIN = 4;
const int ECHO_PIN = 5;

// MQTT Broker Details
const char *mqtt_server = "broker.emqx.io";
const char *mqtt_topic = "SIT210/wave";
const int port = 1883;

WiFiClient wifiClient;
PubSubClient client(wifiClient);
int waveCount = 0;

void setup_wifi()
{
  Serial.print("Connecting to WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi!");
}

void sendEmail()
{
  SMTPSession smtp;
  smtp.debug(1);

  ESP_Mail_Session session;
  session.server.host_name = SMTP_HOST;
  session.server.port = SMTP_PORT;
  session.login.email = AUTHOR_EMAIL;
  session.login.password = AUTHOR_PASSWORD;
  session.login.user_domain = "";

  SMTP_Message message;
  message.sender.name = "Arduino Nano 33 IoT";
  message.sender.email = AUTHOR_EMAIL;
  message.subject = "Wave Alert!";
  message.addRecipient("User", RECIPIENT_EMAIL);
  message.text.content = "Ahmad waved 10 times!";

  if (!smtp.connect(&session))
    return;
  if (!smtp.isLoggedIn())
    return;
  if (!MailClient.sendMail(&smtp, &message))
  {
    Serial.println("Email failed to send");
  }
  else
  {
    Serial.println("Email sent!");
  }
}

void waveBlink()
{
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);
  delay(500);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  delay(500);
}

void patBlink()
{
  digitalWrite(LED1, HIGH);
  delay(200);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, HIGH);
  delay(200);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, HIGH);
  delay(200);
  digitalWrite(LED3, LOW);
}

// Publish gesture message
void publishGesture(String gesture)
{
  client.publish(mqtt_topic, gesture.c_str());
}

// MQTT callback function
void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message received: ");
  String message;
  for (int i = 0; i < length; i++)
  {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (message == "Ahmad Waved")
  {
    waveBlink();
    waveCount++;
    if (waveCount >= 10)
    {
      sendEmail();
      waveCount = 0;
    }
  }
  else if (message == "Ahmad Patted")
  {
    patBlink();
  }
}

String detectGesture()
{
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  int distance = duration * 0.034 / 2; 

  if (distance >= 20 && distance <= 40)
  {
    return "Ahmad Waved"; 
  }
  else if (distance > 0 && distance < 20)
  {
    return "Ahmad Patted"; 
  }

  return ""; 
}

// Setup function
void setup()
{
  Serial.begin(115200);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  setup_wifi();
  client.setServer(mqtt_server, port);
  client.setCallback(callback);

  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ArduinoClient"))
    {
      Serial.println("Connected to MQTT");
      client.subscribe(mqtt_topic);
    }
    else
    {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");
      delay(5000);
    }
  }
}

// Main loop
void loop()
{
  if (!client.connected())
  {
    setup_wifi();
  }
  client.loop();

  String gesture = detectGesture();
  if (gesture != "")
  {
    Serial.println(gesture);
    publishGesture(gesture);
    delay(1000); 
  }
}
