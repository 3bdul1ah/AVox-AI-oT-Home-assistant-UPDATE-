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
from recorder import live_speech
import pickle
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

with open("prompt.json", "r") as f:
    prompt = json.load(f)

default_prompt = prompt["response_format"] + prompt["commands"] + prompt["example_response"] + prompt["no_command_response"] + prompt["inferred_responses"]

if(os.path.exists("history")):
    with open("history", "rb") as fp:
        history = pickle.load(fp)

        chat = model.start_chat(history=history)
else:
    chat = model.start_chat(history=[])
    response = chat.send_message(default_prompt)

def detect_wakeup(command: str, wakeup_words: list[str]):
    command = re.sub(r"[,\.!?]", "", command.lower())

    for word in wakeup_words:
        word = re.sub(r"[,\.!?]", "", word.lower())
        if word in command:
            return True

    return False

def TTSdeepgram(text, filename):
    try:
            SPEAK_OPTIONS = {"text": assistant}
            deepgram = DeepgramClient(api_key= DG_API_KEY)

            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",
                container="wav"
            )

            response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)

    except Exception as e:
            print(f"Exception: {e}")

if not os.path.exists("wakeup_words.json"):
    print("You must run init.py first!")
    sys.exit(1)

with open("wakeup_words.json", "r") as f:
    wakeup_words = json.load(f)
print("Listening...")
woken_up = [False]
while True:
    if(woken_up[0] == False):
        for message in live_speech(woken_up):
            if detect_wakeup(message, wakeup_words):
                print(f"Detected: {message}")
                woken_up[0] = True
                break
    else:
        for message in live_speech(woken_up,60):
            print(message)
            if(message != ''):
                try:
                    response = chat.send_message(message)
                except:
                    response=''
                assistant = response.text

                print(assistant)
                TTSdeepgram(assistant,"assistant.wav")
                os.system("aplay -q assistant.wav")
                history = chat.history
    
                with open("history", "wb") as fp:
                    pickle.dump(history, fp)
                os.remove("assistant.wav")
            break