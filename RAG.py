from langchain import Ollama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_unstructured import UnstructuredLoader
import nltk
import os
from pathlib import Path

nltk.data.path.append("/home/wojzub2/nltk_data")

folder_path = Path("../../texts")

files = [
    p for p in folder_path.rglob("*")
    if p.is_file()
]

loader = UnstructuredLoader(
    files,
    chunking_strategy="basic",
    max_characters=1000,
    include_orig_elements=False,
   )

docs = loader.load()

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="./chroma_db"
)

db.persist()

db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = db.as_retriever(search_kwargs={"k": 5})

llm = Ollama(model="llama3.1")  

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

query = "tell me about emperor of mankind"
print(qa.run(query))

