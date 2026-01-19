# tts_quickfox.py
print("importing libraries")
from TTS.api import TTS

print("loading TTS model")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=True)

text = "The quick brown fox jumps over the lazy dog."
print(f"Text {text}")
print("Saving the generated file")
out_path = "quickfox.wav"
tts.tts_to_file(text=text, file_path=out_path)

print("Playing - through Windows")
import os, subprocess
win_path = subprocess.check_output(["wslpath", "-w", out_path]).decode().strip()
subprocess.run(["cmd.exe", "/C", "start", "", win_path])

