import paho.mqtt.publish as publish

MQTT_SERVER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "input/voice"

def publish_command(message):
    try:
        publish.single(MQTT_TOPIC, payload=message, hostname=MQTT_SERVER, port=MQTT_PORT)
    #    print(f"Published to MQTT: {message}")
    except Exception as e:
        print(f"Failed to publish to MQTT: {e}")