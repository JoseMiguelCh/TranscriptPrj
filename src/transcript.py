"""
This project records audio and transcribes it to text, sending a notification when a
series of keywords are mentioned.

Dependencies:
- sounddevice
- whisper

"""

import os
import json
import whisper
import wavio as wv
import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

i = 0
FREQ = 44100
CLIP_DURATION = 10
FILENAME_TRANSCRIPT = 'transcript.txt'
MODEL = whisper.load_model("base")
KEYWORDS = json.loads(os.getenv("KEYWORDS"))

print("Recording to alert when Im mentioned")
try:
    while True:
        recording_name = f"records/recording{i}.wav"
        recording = sd.rec(int(CLIP_DURATION * FREQ),
                           samplerate=FREQ, channels=1)
        sd.wait()
        wv.write(recording_name, recording, FREQ, sampwidth=2)
        result = MODEL.transcribe(recording_name,  fp16=False)
        i += 1

        with open(FILENAME_TRANSCRIPT, 'a', encoding='UTF-8') as file:
            file.write(result["text"] + '\n')

        if i > 5:
            for j in range(4):
                name = f"records/recording{j}.wav"
                os.remove(name)
            os.rename(f"records/recording{5}.wav", f"records/recording{0}.wav")
            i = 1

        if any(x in result["text"] for x in KEYWORDS):
            os.system(f'terminal-notifier -title "Te nombraron, bb" -message "{result["text"]} grabacion guardada en {recording_name}" -sound default')

except KeyboardInterrupt:
    pass
