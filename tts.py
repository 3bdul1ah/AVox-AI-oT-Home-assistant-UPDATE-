import subprocess
import os


def run_piper(text, model, output_file):
    command = ["piper", "--model", model, "--output_file", output_file]
    
    if os.path.exists(output_file):
        print(f"Output file {output_file} already exists. Removing it.")
        os.remove(output_file)

    try:
        subprocess.run(command, input=text.encode(), check=True, capture_output=True)
        
        playback_status = subprocess.run(["aplay", "-q", output_file], check=True)
        if playback_status.returncode != 0:
            print("An error occurred during audio playback.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

text = ""
model = "en_US-libritts-high.onnx"
output_file = "assistant.wav"

run_piper(text, model, output_file)

