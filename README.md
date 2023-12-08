## IoT Based Voice Controlled Home Automation Using NodeMCU & Raspberry pi
This project combines an ESP32-based home automation system, a voice control module using Python, integrates with Node-RED for additional processing and UI capabilities, and includes DHT22 sensor monitoring through a Raspberry Pi 4 server.

![Project Prototype](https://eu-central.storage.cloudconvert.com/tasks/cb408d4d-df23-465c-9d18-01673c4b2786/b0e7b067-f65e-4900-b5c8-787ba48048a8.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231129%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231129T212016Z&X-Amz-Expires=86400&X-Amz-Signature=3385e149291f3417436314d537f3a3f13d6bcd25fe0b97b3c12c8485ddf4ed86&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22b0e7b067-f65e-4900-b5c8-787ba48048a8.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)
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
![Import Libraries](https://eu-central.storage.cloudconvert.com/tasks/27f8f09b-943f-45b1-bad2-206e89a60363/Screenshot%20from%202023-12-03%2010-03-24.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T021537Z&X-Amz-Expires=86400&X-Amz-Signature=e22520d377b6ce27d6a757ef19e7b8d44bc45634cca4fbde9ef21d7f8234d79b&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-03-24.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

import the necessary libraries: `speech_recognition` for voice recognition, `paho.mqtt.publish` for MQTT communication, and `time` for introducing delays.

### MQTT Configuration
![MQTT Configuration](https://eu-central.storage.cloudconvert.com/tasks/c3c028e9-6b0d-4c47-8857-df49b6b57263/Screenshot%20from%202023-12-03%2010-06-48.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T021105Z&X-Amz-Expires=86400&X-Amz-Signature=d71ecac74785644e5610d82fc573070c527294e3f7b0da1bd447404ccdeddaf1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-06-48.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

sets up the configuration for the MQTT broker, including the server address, port, and the topic to which voice commands will be published.

### Initialize Speech Recognition Module
![Initialize Speech Recognition Module](https://eu-central.storage.cloudconvert.com/tasks/8c8bb79b-dabd-4980-9f18-d2e0d78dfec0/Screenshot%20from%202023-12-03%2010-17-33.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T022259Z&X-Amz-Expires=86400&X-Amz-Signature=4a6ca1c482a8b85d8729edacf591a52fe4248854298fce146d0d1a5a0333583a&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-17-33.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

creates an instance of the `recognizer` class from the `speech_recognition` library to manage speech recognition.

### Listen For Command Function 
![Listen For Command Function ](https://eu-central.storage.cloudconvert.com/tasks/6bb2eab5-0826-4eb2-838a-8b2209ec387f/Screenshot%20from%202023-12-03%2010-20-52.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T022101Z&X-Amz-Expires=86400&X-Amz-Signature=40611933b94777d4b95af0b14d71c6fdab594e7e0359c8ee69e74452475a06bd&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-20-52.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

This function captures audio from the microphone, adjusts for ambient noise, and uses Google Speech Recognition to convert the audio to text. It returns the recognized `command` or `None` if there's an issue.

### Publish Command Function
![Publish Command Function](https://eu-central.storage.cloudconvert.com/tasks/034e564e-6284-4a15-a098-22e2f959a3fa/Screenshot%20from%202023-12-03%2010-26-25.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T022651Z&X-Amz-Expires=86400&X-Amz-Signature=384480a7e22e45f6fce06b5d5c7ec0e0c9c7895559f97e4326b2690e19e4ff07&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-26-25.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

This function publishes the recognized command to `input/voice` MQTT topic in Node-RED using the `publish.single` function.

### Main Execution
![Main Execution](https://eu-central.storage.cloudconvert.com/tasks/7e3a0a11-ba65-4c38-84a7-ef28f2afd45f/Screenshot%20from%202023-12-03%2010-29-17.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T022927Z&X-Amz-Expires=86400&X-Amz-Signature=0e18cdb505259f6c1778aa51ccb4728a62c3390667bf192d27443ecf338bb67a&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-29-17.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

The script enters an infinite loop to continuously listen for voice commands. If a command is recognized, it is published to the MQTT broker. A 2-second delay is added between iterations.


## Node-RED Integration

1. Set up Node-RED with MQTT nodes to receive voice commands from `input/voice`.
2. Process voice commands and implement logic as needed.
3. Use MQTT nodes to publish processed commands to ESP32 MQTT topics.
4. Raspberry Pi 4 serves as the server hosting Node-RED.

![Node-RED Flow](https://eu-central.storage.cloudconvert.com/tasks/29b87eef-e8df-4560-b888-cafd2bae2c9e/Screenshot%20from%202023-12-03%2010-31-44.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T023220Z&X-Amz-Expires=86400&X-Amz-Signature=1e2ce3a651edae8cab2a596b48161f2f3ff803a044d275b62ac40dd1bf23a975&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2010-31-44.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

## IoT Dashboard

1. Create a UI in Node-RED for monitoring and controlling the home automation system.
2. Add dashboard elements for lights and fans in each room.
3. Implement controls and feedback mechanisms based on MQTT data.
4. Display DHT22 sensor readings in the dashboard using appropriate dashboard nodes.
![Dash]()


## Usage

1. Deploy the ESP32 system in your home.
2. Run the Python script on a device with a microphone.
3. Speak voice commands to control lights and fans.
4. Utilize Node-RED on the Raspberry Pi 4 server for additional processing, UI features, and DHT22 sensor monitoring.

Feel free to customize the code and adapt it to your specific home automation setup.

**Note:** Adjust sleep times, timeouts, and other parameters according to your requirements.
