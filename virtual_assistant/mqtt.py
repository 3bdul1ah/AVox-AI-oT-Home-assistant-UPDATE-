import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from pathlib import Path
import json
import sys
import os
import re
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
load_dotenv()
from config import GOOGLE_API_KEY, DG_API_KEY
import pickle
import google.generativeai as genai


MQTT_SERVER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC_PUBLISH = "input/voice"
MQTT_TOPIC_SUBSCRIBE = "Luna/Input"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

with open("prompt.json", "r") as f:
    prompt = json.load(f)

default_prompt = (
    prompt["response_format"] +
    prompt["commands"] +
    prompt["example_response"] +
    prompt["no_command_response"] +
    prompt["inferred_responses"]
)

if(os.path.exists("history")):
    with open("history", "rb") as fp:
        history = pickle.load(fp)

        chat = model.start_chat(history=history)
else:
    chat = model.start_chat(history=[])
    response = chat.send_message(default_prompt)


def TTSdeepgram(text, filename):
    try:
            SPEAK_OPTIONS = {"text": text}
            deepgram = DeepgramClient(api_key= DG_API_KEY)

            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",
                container="wav"
            )

            response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)

    except Exception as e:
            print(f"Exception: {e}")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_SUBSCRIBE)

def publish_command(message):
    try:
        publish.single(MQTT_TOPIC_PUBLISH, payload=message, hostname=MQTT_SERVER, port=MQTT_PORT)
    except Exception as e:
        print(f"Failed to publish to MQTT: {e}")

def Luna_Input(client, userdata, msg):
    voice = msg.payload.decode()
    print(voice)
    response = chat.send_message(voice)
    assistant = response.text
    publish_command(assistant)
    print(assistant)
    TTSdeepgram(assistant,"assistant.wav")
    os.system("aplay -q assistant.wav")
    history = chat.history

    with open("history", "wb") as fp:
        pickle.dump(history, fp)
    os.remove("assistant.wav")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = Luna_Input

client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_forever()
