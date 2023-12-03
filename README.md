# IoT Based Voice Controlled Home Automation Using NodeMCU & Raspberry pi
This project combines an ESP32-based home automation system, a voice control module using Python, integrates with Node-RED for additional processing and UI capabilities, and includes DHT22 sensor monitoring through a Raspberry Pi 4 server.
![Project Prototype](https://eu-central.storage.cloudconvert.com/tasks/cb408d4d-df23-465c-9d18-01673c4b2786/b0e7b067-f65e-4900-b5c8-787ba48048a8.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231129%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231129T212016Z&X-Amz-Expires=86400&X-Amz-Signature=3385e149291f3417436314d537f3a3f13d6bcd25fe0b97b3c12c8485ddf4ed86&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22b0e7b067-f65e-4900-b5c8-787ba48048a8.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)
## ESP32 Home Automation System

### Requirements
- ESP32
- Arduino IDE
- WiFi and MQTT Broker (e.g., broker.emqx.io)
  
## Libraries
![Libraries](https://eu-central.storage.cloudconvert.com/tasks/c11c9ad6-8455-4f49-bd2d-ee36e4594fa0/Screenshot%20from%202023-12-03%2009-21-36.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T012250Z&X-Amz-Expires=86400&X-Amz-Signature=1dc2e61b624ad29c31f4f4116325808f617cb9c45403e2964d271702a7bbfd5d&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-21-36.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

Include essential libraries for Wi-Fi connectivity `WiFi.h` , MQTT communication `PubSubClient.h`, and motor control `L298N.h`.

## Wi-Fi and MQTT Configuration
![Wi-Fi and MQTT Configuration](https://eu-central.storage.cloudconvert.com/tasks/1b08f335-0eb6-468f-9c00-2f3ef1f2adfc/Screenshot%20from%202023-12-03%2009-28-55.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T012907Z&X-Amz-Expires=86400&X-Amz-Signature=a0642e7479b665aa3789f95a2d533e4353562a82de3fde4666e63b1663d831b8&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-28-55.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

sets up Wi-Fi credentials, MQTT broker information, and a unique client ID for the ESP32.

## Room 1 & Room 2 Configuration
![Room 1 & Room 2 Configuration](https://eu-central.storage.cloudconvert.com/tasks/db63e844-5de4-4db5-9bbb-fb5db2fd7e98/Screenshot%20from%202023-12-03%2009-32-16.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231203%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231203T013230Z&X-Amz-Expires=86400&X-Amz-Signature=148c6214b16ee55bda6c3f9b3ed23ab033ddd1bbc150858f1fae247e90770717&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-12-03%2009-32-16.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

defines MQTT topics and pin configurations for both rooms, including light and fan control topics and corresponding pin assignments for the L298N motor driver.



### MQTT Commands
- Light Control: "on", "twentyfive", "fifty", "seventyfive", "off"
- Fan Control: "on", "twentyfive", "fifty", "seventyfive", "off"

## Voice Control Module

### Requirements
- Python
- SpeechRecognition
- paho-mqtt

### Setup
1. Install required Python packages: `pip install SpeechRecognition paho-mqtt`
2. Update MQTT broker information in the Python code.

### Voice Commands
- Speak voice commands, and they will be sent to the MQTT topic: `input/voice`

## Node-RED Integration

1. Set up Node-RED with MQTT nodes to receive voice commands from `input/voice`.
2. Process voice commands and implement logic as needed.
3. Use MQTT nodes to publish processed commands to ESP32 MQTT topics.
4. Raspberry Pi 4 serves as the server hosting Node-RED.

![Node-RED Flow](https://eu-central.storage.cloudconvert.com/tasks/20e8386b-9e7f-4010-8b29-5f9210d74fe3/Screenshot%20from%202023-11-30%2005-13-49.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20231129%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20231129T211400Z&X-Amz-Expires=86400&X-Amz-Signature=4ca1d7b7923cfcd3b04d8a8cfba87b929169c078fa86092136a74460c57be676&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Screenshot%20from%202023-11-30%2005-13-49.webp%22&response-content-type=image%2Fwebp&x-id=GetObject)

## IoT Dashboard

1. Create a UI in Node-RED for monitoring and controlling the home automation system.
2. Add dashboard elements for lights and fans in each room.
3. Implement controls and feedback mechanisms based on MQTT data.
4. Display DHT22 sensor readings in the dashboard using appropriate dashboard nodes.

## Usage

1. Deploy the ESP32 system in your home.
2. Run the Python script on a device with a microphone.
3. Speak voice commands to control lights and fans.
4. Utilize Node-RED on the Raspberry Pi 4 server for additional processing, UI features, and DHT22 sensor monitoring.

Feel free to customize the code and adapt it to your specific home automation setup.

**Note:** Adjust sleep times, timeouts, and other parameters according to your requirements.
