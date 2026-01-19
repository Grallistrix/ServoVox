from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_unstructured import UnstructuredLoader
import nltk
nltk.data.path.append("../../nltk_data")

import os
from pathlib import Path

folder_path = Path("../../texts")

files = [
    p for p in folder_path.rglob("*")
    if p.is_file()
]

loader = UnstructuredLoader(
    files,
    mode="single",
    strategy="fast"
   )

docs = loader.load()

print("Number of LangChain documents:", len(docs))
print("Length of text in the document:", len(docs[0].page_content))