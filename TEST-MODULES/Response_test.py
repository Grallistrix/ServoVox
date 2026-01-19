#import
from TTS.api import TTS
import requests
import whisper
import os, subprocess

model = whisper.load_model("turbo")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.m4a")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

#model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=True)

#prompt
base_prompt = "(You're an archivist servitor in the world of Warhammer 40k, a techpriest in querying you on your knowledge on history of Imperium of Men. Be robotic and swift in reply. Be very accurate. If there things you're unsure or don't know, say [Records Missing]. The asnwers must be short. 3 sentences) "
prompt="Who is  the 5th Chaos God Malal?"
query= base_prompt+result.text

#get ollama response
response = requests.post(
    "http://localhost:11434/v1/completions",
    json={"model": "llama3:latest", "prompt": query}
)
print("Query: "+query+"\n")
print("Response:\n"+response.json()["choices"][0]["text"])

#response to text
text = response.json()["choices"][0]["text"]

print(f"Text {text}")
print("Saving the generated file")
out_path = "quickfox.wav"
tts.tts_to_file(text=text, file_path=out_path)

#play response
print("Playing - through Windows")
win_path = subprocess.check_output(["wslpath", "-w", out_path]).decode().strip()
subprocess.run(["cmd.exe", "/C", "start", "", win_path])

