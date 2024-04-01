from pathlib import Path
import json
import sys
import os
import re
from gtts import gTTS
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
load_dotenv()



from playsound import playsound

from recorder import live_speech
import pickle

# Import the Python SDK
import google.generativeai as genai


GOOGLE_API_KEY="AIzaSyCbmJ8LovRKxh4O-zZ_VbD_1F5sO4ShO8U"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

with open("prompt.json", "r") as f:
    prompt = json.load(f)

default_prompt = prompt["response_format"] + prompt["commands"] + prompt["example_response"] + prompt["no_command_response"] + prompt["inferred_responses"]

if(os.path.exists("history")):
    with open("history", "rb") as fp:
        history = pickle.load(fp)
    # with open('history.json', 'r') as openfile:
    #     history = json.load(openfile)

        chat = model.start_chat(history=history)
else:
    chat = model.start_chat(history=[])
    response = chat.send_message(default_prompt)


# response = chat.send_message(default_prompt)
# response = model.generate_content("You are an AI asistant for IOT Home project and you can reply with either 'room 1 lights on' or 'room 1 lights off' or 'room 2 lights on' or 'room 2 lights off' or 'increase fan speed' or 'decrease fan speed' ")
# print(response.text)

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
            # STEP 1 Create a Deepgram client using the API key from environment variables
            deepgram = DeepgramClient(api_key= "abc5087ea25687bbe6dc634a4316644885aa473f")

            # STEP 3 Configure the options (such as model choice, audio configuration, etc.)
            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",
                container="wav"
            )

            # STEP 2 Call the save method on the speak property
            response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
            # print(response.to_json(indent=4))

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
                # print(strings)
                # if(len(strings) > 1):
                #     command = strings[-1]
                # assistant = strings[0]
                # if(len(strings) > 2):
                #     for i in range(1,len(strings)-1):
                #         assistant += strings[i]
                # print(assistant)
                
                # myobj = gTTS(text=assistant, tld='us', lang='en', slow=False, )
                # myobj.save("assistant.mp3")
                print(assistant)
                TTSdeepgram(assistant,"assistant.wav")
                os.system("aplay -q assistant.wav")
                # engine.say(assistant)
                # engine.runAndWait()
                history = chat.history
    
                # with open("history.json", "w") as outfile:
                #     json.dump(history, outfile)
                with open("history", "wb") as fp:
                    pickle.dump(history, fp)
                #playsound("assistant.mp3")
                os.remove("assistant.wav")
            break
