# uruchomienie

## python 3.11

3.11 pobrane z deadsnakes
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install pytjon3.11
```
uruchomienie
```bash
python3.11 -m venv tts-env
source tts-env/bin/activate
pip install TTS
```

## STT
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -U openai-whisper
sudo apt update && sudo apt install ffmpeg
```
## RAG
``` bash
pip install langchain langchain-ollama langchain-chroma
ollama pull mxbai-embed-large

pip install "langchain-unstructured[local]"
pip install langchain-community
pip install "unstructured[all-docs]"
pip install -U unstructured
```

