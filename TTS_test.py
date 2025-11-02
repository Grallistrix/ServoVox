# tts_quickfox.py
from TTS.api import TTS
import simpleaudio as sa

# Wybierz model (tu przykład dla angielskiego LJSpeech)
print("loading model")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=True)

text = "The quick brown fox jumps over the lazy dog."

print("Saving the generated file")
out_path = "quickfox.wav"
tts.tts_to_file(text=text, file_path=out_path)

print("Playing - through Windows")
import os, subprocess
win_path = subprocess.check_output(["wslpath", "-w", out_path]).decode().strip()
subprocess.run(["cmd.exe", "/C", "start", "", win_path])

