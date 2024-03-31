import pyaudioop as audioop 
# from faster_whisper import WhisperModel
import pyaudio
import wave
import os
import speech_recognition as sr

# model_size = "tiny"
# whisper_model =  WhisperModel(model_size, device="cpu", compute_type="int8")
# ambient_detected = False
speech_volume = 9980


r = sr.Recognizer()

def live_speech(woken_up, wait_time=10):
    global ambient_detected
    global speech_volume
    audio = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    CHUNK = 1024

    

    # info = audio.get_host_api_info_by_index(0)
    # numdevices = info.get('deviceCount')
    # for i in range(0, numdevices):
    #     if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #         print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i))

   

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    recording = False
    frames_recorded = 0
    silence_buffer = 0
    recording_stop = False
   
    while True:
        frames_recorded += 1
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)
     #  print(rms)

        # if not ambient_detected:
        #     if frames_recorded < 10:
        #         if frames_recorded == 1:
        #             print("Detecting ambient noise...")
        #         if frames_recorded > 5:
        #             if speech_volume < rms:
        #                 speech_volume = rms
        #         continue
        #     elif frames_recorded == 10:
        #         print("Listening...")
        #         speech_volume = speech_volume * 1.2
        #         ambient_detected = True

        if(rms < speech_volume and recording):
            silence_buffer+=1
            if(silence_buffer > 10):
                recording_stop = True

        if(frames_recorded > wait_time and not recording):
            woken_up[0] = False
            yield ""
                

        if rms > speech_volume:
            recording = True
            frames_recorded = 0
            silence_buffer = 0
            recording_stop = False
        elif recording and recording_stop:
            recording = False

            wf = wave.open("audio.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            try:
                audiofile = sr.AudioFile("audio.wav")
                with audiofile as source:
                        # r.adjust_for_ambient_noise(source)
                        audio_rec = r.record(source)
                result = r.recognize_google(audio_rec)
            except sr.UnknownValueError:
                result = ""

            # result, _ = whisper_model.transcribe("audio.wav")
            #result = list(result)
            # result = result.split(" ")
            # 

            # result = whisper_model.transcribe(
            #     "audio.wav",
            #     fp16=False
            # )

            os.remove("audio.wav")
            frames = []
            if(len(result) > 0):
                # yield result[0].text.strip()
                yield result
            else:
                yield ""

            frames = []

        if recording:
            frames.append(data)

