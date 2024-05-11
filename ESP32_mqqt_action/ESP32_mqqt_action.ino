#include <WiFi.h>
#include <PubSubClient.h>
#include <L298N.h>
#include <ESP32Servo.h>

const char* ssid = "Xiaomi 12 Lite";
const char* password = "12345678";

const char* mqttServer = "broker.emqx.io";
const int mqttPort = 1883;
const char* clientId = "ESP32";

const char* lightTopicRoom1 = "Home/Room1/Light";
const char* lightTopicRoom2 = "Home/Room2/Light";
const char* fanTopicRoom1 = "Home/Room1/Fan";
const char* fanTopicRoom2 = "Home/Room2/Fan";
const char* doorTopic = "Home/Door";

const int lightPinRoom1 = 14;
const int enAFanRoom1 = 27;   
const int in1FanRoom1 = 26;   
const int in2FanRoom1 = 25;   
L298N fanMotorRoom1(enAFanRoom1, in1FanRoom1, in2FanRoom1);

const int lightPinRoom2 = 21;  
const int enAFanRoom2 = 19;    
const int in1FanRoom2 = 18;    
const int in2FanRoom2 = 5;    
L298N fanMotorRoom2(enAFanRoom2, in1FanRoom2, in2FanRoom2);

WiFiClient espClient;
PubSubClient client(espClient);
Servo myservo;

void callback(char* topic, byte* payload, unsigned int length)
{
  String payloadStr = "";
  for (int i = 0; i < length; i++) {
    payloadStr += (char)payload[i];
  }


  if (String(topic) == lightTopicRoom1)
   handleLightControl(payloadStr, lightPinRoom1);

  if (String(topic) == fanTopicRoom1) 
   handleFanControl(payloadStr, fanMotorRoom1); 
   
  if (String(topic) == lightTopicRoom2)
   handleLightControl(payloadStr, lightPinRoom2);

  if (String(topic) == fanTopicRoom2) 
   handleFanControl(payloadStr, fanMotorRoom2); 

  if (String(topic) == doorTopic) 
   handleDoorControl(payloadStr); 

} 

void handleDoorControl(String payload){
  if(payload.equals("open")){
    myservo.write(0);
  }else if(payload.equals("close")){
    myservo.write(140);
  }
}

void handleLightControl(String payload, int lightPin) {

  if (payload.equals("on")) {
    analogWrite(lightPin, 255);

  }  else if (payload.equals("twentyfive")) {
    analogWrite(lightPin, 64);

  } else if (payload.equals("fifty")) {
    analogWrite(lightPin, 128); 

  } else if (payload.equals("seventyfive")) {
    analogWrite(lightPin, 192);
  
  } else if (payload.equals("off")) {
    analogWrite(lightPin, 0);
  

  }
}

void handleFanControl(String payload, L298N& fanMotor) {

  if (payload.equals("on")) {
    fanMotor.setSpeed(160); 
    fanMotor.forward();

  } else if (payload.equals("twentyfive")) {
    fanMotor.setSpeed(64); 
    fanMotor.forward();

  } else if (payload.equals("fifty")) {
    fanMotor.setSpeed(128); 
    fanMotor.forward();

  } else if (payload.equals("seventyfive")) {
    fanMotor.setSpeed(140); 
    fanMotor.forward();
  
  } else if (payload.equals("off")) {
    fanMotor.stop();
  }
}

void setup() {

  Serial.begin(115200);
  myservo.attach(4);
  myservo.write(140);
  analogWrite(lightPinRoom2, 0);
  analogWrite(lightPinRoom1, 0);
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
      client.subscribe(doorTopic);
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
        client.subscribe(doorTopic);
      } else {
        Serial.println("Failed to reconnect to MQTT Broker, trying again in 5 seconds...");
        delay(5000);
      }
    }
  }
  client.loop();
}