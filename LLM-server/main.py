# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import whisper
from TTS.api import TTS
import torch
import requests
import os
import uuid


from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    
### LANGCHAIN libraries
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
### 

### RAG libraries
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
###

### RAG retriever
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_exist =  os.path.exists("chroma_db")

db = Chroma(
    persist_directory="chroma_db",
    embedding_function = embeddings    
)

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8}
    )
###

app = FastAPI(title="Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # na start, potem zawęż
    allow_credentials=True,
    allow_methods=["*"],  # MUSI zawierać OPTIONS
    allow_headers=["*"],
)

# --- MODELS ---
print("Loading Whisper model...")
whisper_model = whisper.load_model("turbo")

print("Loading TTS model...")
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=torch.cuda.is_available())

OLLAMA_URL = "http://localhost:11434/v1/completions"
OLLAMA_MODEL = "llama3.1:8b"

### Prompt
prompt = PromptTemplate(
    template="""
You're an archivist servitor in the world of Warhammer 40k, a techpriest in querying you on your knowledge on history of Imperium of Men.
Be robotic and swift in reply. 
Be very accurate.
If there things you're unsure or don't know, say [Records Missing]. 
The answer must be short, 3 to 4 sentences.

Retrieved Context from Archives:
{context}

Question:
{question}

Response:
""",
    input_variables=["context", "question"],
)

### Model
llm = ChatOllama(model="llama3")

### Wywołanie
qa_chain = prompt | llm


# --- UTILS ---

# def call_ollama(prompt: str):
#     """Send prompt to Ollama and return response text"""
#     response = requests.post(
#         OLLAMA_URL,
#         json={"model": OLLAMA_MODEL, "prompt": prompt}
#     )
#     response.raise_for_status()
#     return response.json().get("completion") or response.json()

def call_ollama(prompt: str):
    """Send prompt to Ollama and return response text"""
    re_data = retriever.invoke(prompt)
    context = "\n\n".join([r.page_content for r in re_data])
    response = qa_chain.invoke({"context": context, "question": prompt})
    return response.content


def stt_from_audio_file(file_path: str):
    """Convert audio file to text using Whisper"""
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio, n_mels=whisper_model.dims.n_mels).to(whisper_model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(whisper_model, mel, options)
    return result.text


def tts_to_file(text: str, file_path: str):
    """Generate TTS audio file from text"""
    tts_model.tts_to_file(text=text, file_path=file_path)
    return file_path


# --- ENDPOINTS ---

# 1. Text -> Text
@app.post("/text_to_text")
def text_to_text(req: TextRequest):
    prompt = req.text
    reply = call_ollama(prompt)
    return {"text": reply}

# 2. Text -> Audio
@app.post("/text_to_audio")
def text_to_audio(prompt: str):
    reply_text = call_ollama(prompt)
    out_file = f"tts_{uuid.uuid4().hex}.wav"
    tts_to_file(reply_text, out_file)
    return FileResponse(out_file, media_type="audio/wav", filename="response.wav")

# 2b. Test version
#@app.post("/test_text_to_audio")
#def test_text_to_audio(prompt: str):
#    print(f"Received prompt: {prompt}")
#    out_file = f"tts_test_{uuid.uuid4().hex}.wav"
#    tts_to_file(prompt, out_file)  # just speak the prompt itself
#    return FileResponse(out_file, media_type="audio/wav", filename="test.wav")


# 3. Audio -> Text
@app.post("/audio_to_text")
async def audio_to_text(file: UploadFile = File(...)):
    temp_file = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())
    text = stt_from_audio_file(temp_file)
    os.remove(temp_file)
    return {"recognized_text": text}

# 3b. Test version
@app.post("/test_audio_to_text")
async def test_audio_to_text(file: UploadFile = File(...)):
    temp_file = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())
    text = stt_from_audio_file(temp_file)
    os.remove(temp_file)
    print(f"Recognized text: {text}")
    return {"recognized_text": text, "mode": "TEST_MODE"}


# 4. Audio -> Audio
@app.post("/audio_to_audio")
async def audio_to_audio(file: UploadFile = File(...)):
    # Save uploaded file
    temp_file = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # STT
    text = stt_from_audio_file(temp_file)
    os.remove(temp_file)

    # Call Ollama
    reply_text = call_ollama(text)

    # TTS
    out_file = f"tts_{uuid.uuid4().hex}.wav"
    tts_to_file(reply_text, out_file)

    return FileResponse(out_file, media_type="audio/wav", filename="response.wav")

# 4b. Test version
@app.post("/test_audio_to_audio")
async def test_audio_to_audio(file: UploadFile = File(...)):
    temp_file = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())
    text = stt_from_audio_file(temp_file)
    os.remove(temp_file)
    print(f"Recognized text: {text}")
    # just speak recognized text
    out_file = f"tts_test_{uuid.uuid4().hex}.wav"
    tts_to_file(text, out_file)
    return FileResponse(out_file, media_type="audio/wav", filename="test.wav")
