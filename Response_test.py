from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=True)

base_prompt = "(You're an archivist servitor in the world of Warhammer 40k, a techpriest in querying you on your knowledge on history of Imperium of Men. Be robotic and swift in reply. Be very accurate. If there things you're unsure or don't know, say [Records Missing]. The asnwers must be short. 3 sentences) "
prompt="Who is  the 5th Chaos God Malal?"
query= base_prompt+prompt

response = requests.post(
    "http://localhost:11434/v1/completions",
    json={"model": "llama3.1:8b", "prompt": query}
)
print("Query: "+query+"\n")
print("Response:\n"+response.json()["choices"][0]["text"])

text = response.json()["choices"][0]["text"]

print(f"Text {text}")
print("Saving the generated file")
out_path = "quickfox.wav"
tts.tts_to_file(text=text, file_path=out_path)

print("Playing - through Windows")
import os, subprocess
win_path = subprocess.check_output(["wslpath", "-w", out_path]).decode().strip()
subprocess.run(["cmd.exe", "/C", "start", "", win_path])

