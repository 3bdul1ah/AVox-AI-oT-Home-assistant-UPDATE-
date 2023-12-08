## IoT Based Voice Controlled Home Automation Using NodeMCU & Raspberry pi
This project combines an ESP32-based home automation system, a voice control module using Python, integrates with Node-RED for additional processing and UI capabilities, and includes DHT22 sensor monitoring through a Raspberry Pi 4 server.

![Project Prototype](https://eu-central.storage.cloudconvert.com/tasks/cb408d4d-df23-465c-9d18-01673c4b2786/b0e7b067-f65e-4900-b5c8-787ba48048a8.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231129%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231129T212016Z&X-Amz-Expires=86400&X-Amz-Signature=3385e149291f3417436314d537f3a3f13d6bcd25fe0b97b3c12c8485ddf4ed86&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22b0e7b067-f65e-4900-b5c8-787ba48048a8.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)
## ESP32 Home Automation System

### Requirements
- ESP32
- Arduino IDE
    
### Libraries
<pre>
```
#include <WiFi.h>
#include <PubSubClient.h>
#include <L298N.h>

```
</pre>
Include essential libraries for Wi-Fi connectivity `WiFi.h` , MQTT communication `PubSubClient.h`, and motor control `L298N.h`.

### Wi-Fi and MQTT Configuration
![Wi-Fi and MQTT Configuration](https://eu-central.storage.cloudconvert.com/tasks/1b08f335-0eb6-468f-9c00-2f3ef1f2adfc/Screenshot%20from%202023-12-03%2009-28-55.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T012907Z&X-Amz-Expires=86400&X-Amz-Signature=a0642e7479b665aa3789f95a2d533e4353562a82de3fde4666e63b1663d831b8&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-28-55.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

sets up Wi-Fi credentials, MQTT broker information, and a unique client ID for the ESP32.

### Room 1 & Room 2 Configuration
![Room 1 & Room 2 Configuration](https://eu-central.storage.cloudconvert.com/tasks/db63e844-5de4-4db5-9bbb-fb5db2fd7e98/Screenshot%20from%202023-12-03%2009-32-16.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T013230Z&X-Amz-Expires=86400&X-Amz-Signature=148c6214b16ee55bda6c3f9b3ed23ab033ddd1bbc150858f1fae247e90770717&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-32-16.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

defines MQTT topics and pin configurations for both rooms, including light and fan control topics and corresponding pin assignments for the L298N motor driver.

### Objects Initialization
![Objects Initialization](https://eu-central.storage.cloudconvert.com/tasks/9a9603b0-788e-4bf4-8b95-4336df5b0571/Screenshot%20from%202023-12-03%2009-36-34.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T013717Z&X-Amz-Expires=86400&X-Amz-Signature=df6639def8f979465c627e00e89c4096546f8bfa6913f50a0ded54f07f85c039&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-36-34.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

create instances of the `WiFiClient` and `PubSubClient` classes to handle Wi-Fi and MQTT communication, respectively.

### Callback Function
![Callback Function](https://eu-central.storage.cloudconvert.com/tasks/6bd69c58-42c5-4eb2-93fc-faea591c42a5/Screenshot%20from%202023-12-03%2009-44-39.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T014450Z&X-Amz-Expires=86400&X-Amz-Signature=7ca03217259731901948c4991332d73371d54c5851c4347c9fb7d299fcc2d5a2&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-44-39.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

This function is invoked when an MQTT message is received. It parses the topic and payload, calling the appropriate functions for light or fan control.

### Light and Fan Control Functions
![Light and Fan Control Functions](https://eu-central.storage.cloudconvert.com/tasks/a64b844d-c746-4806-8c29-3c1b43161835/Screenshot%20from%202023-12-03%2009-45-48.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T014602Z&X-Amz-Expires=86400&X-Amz-Signature=4869b5c974806a76ea5690005647f9d1c8ba65ddd9d8ecdadc375d3f7feb52b3&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-45-48.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

These functions handle the logic for controlling lights and fan speed based on the received MQTT payload.

### Setup Function
![Setup Function](https://eu-central.storage.cloudconvert.com/tasks/51690f43-30c7-419c-8bd0-9c2eee29ec1b/Screenshot%20from%202023-12-03%2009-57-18.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T021451Z&X-Amz-Expires=86400&X-Amz-Signature=b5a5bbb0d98714830ec0120847ae9088a77bbf2bc05acae3342ba203e59ecaf1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-57-18.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

The setup function establishes serial communication for debugging, connects to the `Wi-Fi` network, configures the `MQTT client` with the broker's details, and subscribes to relevant topics. It includes mechanisms for retrying connection to both Wi-Fi and MQTT in case of failures.

### Loop Function
![Loop Function](https://eu-central.storage.cloudconvert.com/tasks/7737e0c8-d354-47b4-8f6f-55a466c26319/Screenshot%20from%202023-12-03%2009-59-12.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T021409Z&X-Amz-Expires=86400&X-Amz-Signature=89e1a0e3f8180bad47456eb841844916be3355defb44f406cb76c03f63652ab0&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-59-12.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

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
