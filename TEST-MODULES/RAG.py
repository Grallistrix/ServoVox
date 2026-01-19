from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
#import nltk
import os
from pathlib import Path

#nltk.data.path.append("/home/wojzub2/nltk_data")

# Dostęp do plików
folder_path = Path("../../../texts")

files = [
    p for p in folder_path.rglob("*")
    if p.is_file()
]

# Ładowanie plików
loader = UnstructuredLoader(
    files[0:10],
    chunking_strategy="basic",
    max_characters=1000,
    include_orig_elements=False,
   )

docs = loader.load()

clean_docs = filter_complex_metadata(docs)

# Embedding do bazy
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_exist = os.path.exists("../chroma_db")

if db_exist:
    db = Chroma(
        persist_directory="../chroma_db",
        embedding_function = embeddings    
    )
else: 
    db = Chroma.from_documents(
        clean_docs,
        embeddings,
        persist_directory="../chroma_db"
    )

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6}
    )



