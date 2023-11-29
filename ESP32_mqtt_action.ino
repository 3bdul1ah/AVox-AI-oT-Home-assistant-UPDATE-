#include <WiFi.h>
#include <PubSubClient.h>
#include <L298N.h>

const char* ssid = "";
const char* password = "";

const char* mqttServer = "broker.emqx.io";
const int mqttPort = 1883;
const char* clientId = "ESP32";

const char* room1Topic = "Home/Room1";
const char* lightTopicRoom1 = "Home/Room1/Light";
const char* fanTopicRoom1 = "Home/Room1/Fan";
const int lightPinRoom1 = 32;
const int enAFanRoom1 = 13;   
const int in1FanRoom1 = 12;   
const int in2FanRoom1 = 14;   
L298N fanMotorRoom1(enAFanRoom1, in1FanRoom1, in2FanRoom1);
bool lightStatusRoom1 = false;

const char* room2Topic = "Home/Room2";
const char* lightTopicRoom2 = "Home/Room2/Light";
const char* fanTopicRoom2 = "Home/Room2/Fan";
const int lightPinRoom2 = 35;  
const int enAFanRoom2 = 15;    
const int in1FanRoom2 = 2;    
const int in2FanRoom2 = 4;    
L298N fanMotorRoom2(enAFanRoom2, in1FanRoom2, in2FanRoom2);
bool lightStatusRoom2 = false;

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String payloadStr = "";
  for (int i = 0; i < length; i++) {
    payloadStr += (char)payload[i];
  }

  if (String(topic) == lightTopicRoom1) {
    handleLightControl(payloadStr, lightPinRoom1, lightStatusRoom1);
  } else if (String(topic) == fanTopicRoom1) {
    handleFanControl(payloadStr, fanMotorRoom1);
  } else if (String(topic) == lightTopicRoom2) {
    handleLightControl(payloadStr, lightPinRoom2, lightStatusRoom2);
  } else if (String(topic) == fanTopicRoom2) {
    handleFanControl(payloadStr, fanMotorRoom2);
  }
}

void handleLightControl(String payload, int lightPin, bool& lightStatus) {
  if (payload.equals("on") && !lightStatus) {
    digitalWrite(lightPin, HIGH);
    lightStatus = true;
  } else if (payload.equals("twentyfive")) {
    analogWrite(lightPin, 64);
    lightStatus = true;
  } else if (payload.equals("fifty")) {
    analogWrite(lightPin, 128); 
    lightStatus = true;
  } else if (payload.equals("seventyfive")) {
    analogWrite(lightPin, 192);
    lightStatus = true;
  } else if (payload.equals("off") && lightStatus) {
    digitalWrite(lightPin, LOW);
    lightStatus = false;
  } 
}


void handleFanControl(String payload, L298N& fanMotor) {
  if (payload.equals("on")) {
    fanMotor.setSpeed(255); 
    fanMotor.forward();
  } else if (payload.equals("twentyfive")) {
    fanMotor.setSpeed(64); 
    fanMotor.forward();
  } else if (payload.equals("fifty")) {
    fanMotor.setSpeed(128); 
    fanMotor.forward();
  } else if (payload.equals("seventyfive")) {
    fanMotor.setSpeed(192); 
    fanMotor.forward();
  } else if (payload.equals("off")) {
    fanMotor.stop();
  }
}

void setup() {
  pinMode(lightPinRoom1, OUTPUT);
  pinMode(lightPinRoom2, OUTPUT);

  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Trying to connect to WiFi...");
  }
  Serial.println("Successfully connected to WiFi");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Attempting to connect to MQTT Broker...");
    if (client.connect(clientId)) {
      Serial.println("Connected to MQTT Broker");
      client.subscribe(lightTopicRoom1);
      client.subscribe(fanTopicRoom1);
      client.subscribe(lightTopicRoom2);
      client.subscribe(fanTopicRoom2);
    } else {
      Serial.println("Failed to connect to MQTT Broker, trying again in 5 seconds...");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    Serial.println("Connection lost. Attempting to reconnect...");
    while (!client.connected()) {
      Serial.println("Attempting MQTT reconnection...");
      if (client.connect(clientId)) {
        Serial.println("Reconnected to MQTT Broker");
        client.subscribe(lightTopicRoom1);
        client.subscribe(fanTopicRoom1);
        client.subscribe(lightTopicRoom2);
        client.subscribe(fanTopicRoom2);
      } else {
        Serial.println("Failed to reconnect to MQTT Broker, trying again in 5 seconds...");
        delay(5000);
      }
    }
  }
  client.loop();
}