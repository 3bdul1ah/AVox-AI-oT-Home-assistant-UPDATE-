## IoT Based Voice Controlled Home Automation Using NodeMCU & Raspberry pi
This project combines an ESP32-based home automation system, a voice control module using Python, integrates with Node-RED for additional processing and UI capabilities, and includes DHT22 sensor monitoring through a Raspberry Pi 4 server.

## Table of Contents
- [System Architecture](#sa)
- [Prototype](#pr)
- [ESP32 Home Automation System](#ehas)
- [Node-RED Integration](#nri)
- [Usage](#us)


## System Architecture 
<p align="center">
    <img src="https://i.postimg.cc/WbZwFYBm/image.png">
</p>
The system architecture flowchart outlines the ESP32 setup, MQTT communication, and control functions for light and fan. Simultaneously, a Python Voice Control Module listens for voice commands, and Node-RED integrates voice commands into the ESP32 system, presenting an IoT dashboard for monitoring.


## Prototype
<p align="center">
    <img src="https://i.postimg.cc/qq2s6zNc/image.png">
</p>

The prototype involves wiring lights and DC motors (acting as fans) for two rooms, utilizing a motor driver to control fan speed. Each component represents a room, and the motor driver manages two DC motors simultaneously.

## ESP32 Home Automation System

### Requirements
- ESP32
- Arduino IDE
    
### Libraries
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <L298N.h>
```
Include essential libraries for Wi-Fi connectivity `WiFi.h` , MQTT communication `PubSubClient.h`, and motor control `L298N.h`.

### Wi-Fi and MQTT Configuration
```cpp
const char* ssid = "";
const char* password = "";

const char* mqttServer = "broker.emqx.io";
const int mqttPort = 1883;
const char* clientId = "ESP32";
```
sets up Wi-Fi credentials, MQTT broker information, and a unique client ID for the ESP32.

### Room 1 & Room 2 Configuration
```cpp
const char* room1Topic = "Home/Room1";
const char* lightTopicRoom1 = "Home/Room1/Light";
const char* fanTopicRoom1 = "Home/Room1/Fan";
const int lightPinRoom1 = 26;
const int enAFanRoom1 = 13;   
const int in1FanRoom1 = 12;   
const int in2FanRoom1 = 14;   
L298N fanMotorRoom1(enAFanRoom1, in1FanRoom1, in2FanRoom1);

const char* room2Topic = "Home/Room2";
const char* lightTopicRoom2 = "Home/Room2/Light";
const char* fanTopicRoom2 = "Home/Room2/Fan";
const int lightPinRoom2 = 33;  
const int enAFanRoom2 = 15;    
const int in1FanRoom2 = 2;    
const int in2FanRoom2 = 4;    
L298N fanMotorRoom2(enAFanRoom2, in1FanRoom2, in2FanRoom2);
```
defines MQTT topics and pin configurations for both rooms, including light and fan control topics and corresponding pin assignments for the L298N motor driver.

### Objects Initialization
```cpp
WiFiClient espClient;
PubSubClient client(espClient);
```
create instances of the `WiFiClient` and `PubSubClient` classes to handle Wi-Fi and MQTT communication, respectively.

### Callback Function
```cpp
void callback(char* topic, byte* payload, unsigned int length) {
  String payloadStr = "";
  for (int i = 0; i < length; i++) {
    payloadStr += (char)payload[i];
  }

  if (String(topic) == lightTopicRoom1) {

    handleLightControl(payloadStr, lightPinRoom1);
  } else if (String(topic) == fanTopicRoom1) {
    
    handleFanControl(payloadStr, fanMotorRoom1);
  } else if (String(topic) == lightTopicRoom2) {

    handleLightControl(payloadStr, lightPinRoom2);
  } else if (String(topic) == fanTopicRoom2) {
    handleFanControl(payloadStr, fanMotorRoom2);
  }
}
```
This function is invoked when an MQTT message is received. It parses the topic and payload, calling the appropriate functions for light or fan control.

### Light and Fan Control Functions
```cpp
oid handleLightControl(String payload, int lightPin) {

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

```
These functions handle the logic for controlling lights and fan speed based on the received MQTT payload.

### Setup Function
```cpp
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

```
The setup function establishes serial communication for debugging, connects to the `Wi-Fi` network, configures the `MQTT client` with the broker's details, and subscribes to relevant topics. It includes mechanisms for retrying connection to both Wi-Fi and MQTT in case of failures.

### Loop Function
```cpp
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
```
The loop function continuously checks the `MQTT client's` connection status. If a disconnection is detected, it attempts to reconnect to the MQTT broker, subscribing to topics upon success. The loop also calls `client.loop()` to maintain the MQTT connection and handle incoming messages.


## Voice Control Module

### Requirements
- Python
- SpeechRecognition
- paho-mqtt

### Setup
Install required Python packages: `pip install SpeechRecognition paho-mqtt`

### Import Libraries
```py
import speech_recognition as sr
import paho.mqtt.publish as publish
import time
```
import the necessary libraries: `speech_recognition` for voice recognition, `paho.mqtt.publish` for MQTT communication, and `time` for introducing delays.

### MQTT Configuration
```py
mqtt_server = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic = "input/voice"
```
sets up the configuration for the MQTT broker, including the server address, port, and the topic to which voice commands will be published.

### Initialize Speech Recognition Module
```py
recognizer = sr.Recognizer()
```
creates an instance of the `recognizer` class from the `speech_recognition` library to manage speech recognition.

### Listen For Command Function 
```py
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)  

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return None
```
This function captures audio from the microphone, adjusts for ambient noise, and uses Google Speech Recognition to convert the audio to text. It returns the recognized `command` or `None` if there's an issue.

### Publish Command Function
```py
def publish_command(command):
    publish.single(mqtt_topic, payload=command, hostname=mqtt_server, port=mqtt_port)
```

This function publishes the recognized command to `input/voice` MQTT topic in Node-RED using the `publish.single` function.

### Main Execution
```py
if __name__ == "__main__":
    while True:
        voice_command = listen_for_command()

        if voice_command:
            publish_command(voice_command)
        
        time.sleep(2) 
```

The script enters an infinite loop to continuously listen for voice commands. If a command is recognized, it is published to the MQTT broker. A 2-second delay is added between iterations.


## Node-RED Integration

1. Set up Node-RED with MQTT nodes to receive voice commands from `input/voice`.
2. Process voice commands and implement logic as needed.
3. Use MQTT nodes to publish processed commands to ESP32 MQTT topics.
4. Raspberry Pi 4 serves as the server hosting Node-RED.

<p align="center">
    <img src="https://i.postimg.cc/PqJjHmDp/894fdfc8-4714-4fd8-b8aa-6271c29ae1e1.jpg">
</p>

### IoT Dashboard

1. Create a UI in Node-RED for monitoring and controlling the home automation system.
2. Add dashboard elements for lights and fans in each room.
3. Implement controls and feedback mechanisms based on MQTT data.
4. Display DHT22 sensor readings in the dashboard using appropriate dashboard nodes.

<p align="center">
    <img src="https://i.postimg.cc/KzcgxpN7/image.png">
</p>

## Usage

1. Deploy the ESP32 system in your home.
2. Run the Python script on a device with a microphone.
3. Speak voice commands to control lights and fans.
4. Utilize Node-RED on the Raspberry Pi 4 server for additional processing, UI features, and DHT22 sensor monitoring.

Feel free to customize the code and adapt it to your specific home automation setup.

**Note:** Adjust sleep times, timeouts, and other parameters according to your requirements.
