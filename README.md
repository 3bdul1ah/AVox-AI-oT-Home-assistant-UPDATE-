# IoT-Based-Voice-Controlled-Home-Automation-Using-NodeMCU-andRaspberry-pi

This project combines an ESP32-based home automation system, a voice control module using Python, integrates with Node-RED for additional processing and UI capabilities, and includes DHT22 sensor monitoring through a Raspberry Pi 4 server.

## ESP32 Home Automation System

### Requirements
- ESP32
- Arduino IDE
- WiFi and MQTT Broker (e.g., broker.emqx.io)

### Libraries Used
- WiFi.h
- PubSubClient.h
- L298N.h

### ESP32 Setup
1. Connect the necessary components (lights, fans) to the ESP32.
2. Update the WiFi credentials and MQTT broker information in the code.
3. Flash the code to the ESP32 using the Arduino IDE.

### MQTT Topics
- Room 1: `Home/Room1`, `Home/Room1/Light`, `Home/Room1/Fan`
- Room 2: `Home/Room2`, `Home/Room2/Light`, `Home/Room2/Fan`

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

[Node-RED Flow](file:///home/abdullah/Downloads/Screenshot%20from%202023-11-30%2005-13-49.webp)

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
