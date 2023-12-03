import speech_recognition as sr
import paho.mqtt.publish as publish
import time

mqtt_server = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic = "input/voice"

recognizer = sr.Recognizer()

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

def publish_command(command):
    publish.single(mqtt_topic, payload=command, hostname=mqtt_server, port=mqtt_port)

if __name__ == "__main__":
    while True:
        voice_command = listen_for_command()

        if voice_command:
            publish_command(voice_command)
        
        time.sleep(2)  
