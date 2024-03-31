from pathlib import Path
import json
import sys
import os
import re
from gtts import gTTS
from playsound import playsound

from recorder import live_speech

import google.generativeai as genai
from config import API_KEY

from mqtt import publish_command

GOOGLE_API_KEY= API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

with open("prompt.json", "r") as f:
    prompt = json.load(f)

chat = model.start_chat(history=[])

commands_str = ", ".join(prompt["commands"])

default_prompt = (prompt["response_format"] + commands_str + prompt["example_response"] + 
                  prompt["no_command_response"] + prompt["inferred_responses"] + 
                  prompt["learning_from_history"] + prompt["error_correction"] + 
                  prompt["voice_command_nuances"])

response = chat.send_message(default_prompt)

def detect_wakeup(command: str, wakeup_words: list[str]):
    command = re.sub(r"[,\.!?]", "", command.lower())

    for word in wakeup_words:
        word = re.sub(r"[,\.!?]", "", word.lower())
        if word in command:
            return True

    return False

if not os.path.exists("wakeup_words.json"):
    print("You must run init.py first!")
    sys.exit(1)

with open("wakeup_words.json", "r") as f:
    wakeup_words = json.load(f)
print("Listening...")
woken_up = [False,False]
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
                strings = response.text.split(":")
                # print(strings)
                if(len(strings) > 1):
                    command = strings[-1]
                assistant = strings[0]
                if(len(strings) > 2):
                    for i in range(1,len(strings)-1):
                        assistant += strings[i]
                # print(assistant)
                myobj = gTTS(text=assistant, tld='us', lang='en', slow=False, ) 
                myobj.save("assistant.mp3")
                print(assistant)
                publish_command(assistant)
                # os.system("mpg123 assistant.mp3")
                playsound("assistant.mp3")
                os.remove("assistant.mp3")                
            break


