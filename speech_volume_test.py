# import pyaudioop as audioop
# from faster_whisper import WhisperModel
# import pyaudio
# import wave
# import os

# model_size = "tiny"
# whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")
# ambient_detected = False
# speech_volume = 840  # Default speech volume

# def live_speech(woken_up=[False], wait_time=30):
#     global ambient_detected
#     global speech_volume
#     audio = pyaudio.PyAudio()
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 2
#     RATE = 16000
#     CHUNK = 1024

#     stream = audio.open(
#         format=FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         input=True,
#         frames_per_buffer=CHUNK
#     )

#     def adjust_speech_volume():
#         global speech_volume
#         print("Adjusting speech volume based on ambient noise...")
#         total_rms = 0
#         samples = 10
#         for _ in range(samples):
#             data = stream.read(CHUNK)
#             rms = audioop.rms(data, 2)
#             total_rms += rms
#         average_rms = total_rms / samples
#         speech_volume = average_rms * 1.5  # Adjust threshold based on your needs
#         print(f"Adjusted speech volume to: {speech_volume}")

#     frames = []
#     recording = False
#     frames_recorded = 0
#     silence_buffer = 0
#     recording_stop = False

#     adjust_speech_volume()  # Initial adjustment before starting the loop

#     while True:
#         frames_recorded += 1
#         data = stream.read(CHUNK)
#         rms = audioop.rms(data, 2)
#         print(rms)

#         if rms < speech_volume and recording:
#             silence_buffer += 1
#             if silence_buffer > 10:
#                 recording_stop = True

#         if frames_recorded > wait_time and not recording:
#             woken_up[0] = False
#             yield ""

#         if rms > speech_volume:
#             recording = True
#             frames_recorded = 0
#             silence_buffer = 0
#             recording_stop = False
#         elif recording and recording_stop:
#             recording = False

#             wf = wave.open("audio.wav", 'wb')
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(audio.get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
#             wf.close()

#             result, _ = whisper_model.transcribe("audio.wav")
#             result = list(result)

#             os.remove("audio.wav")
#             frames = []
#             if len(result) > 0:
#                 yield result[0].text.strip()
#             else:
#                 yield ""

#             frames = []
#             adjust_speech_volume()  # Adjust again after each recording

#         if recording:
#             frames.append(data)
