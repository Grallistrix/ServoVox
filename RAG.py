from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

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
    mode="single",
    strategy="fast"
   )
pages = []
for doc in loader.lazy_load():
    pages.append(doc)

pages[0]
#docs = loader.load()

print("Number of LangChain documents:", len(docs))
print("Length of text in the document:", len(docs[0].page_content))