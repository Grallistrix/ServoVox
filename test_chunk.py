from langchain_unstructured import UnstructuredLoader
from langchain_unstructured import UnstructuredLoader
from unstructured.cleaners.core import clean_extra_whitespace
import nltk
import os
from pathlib import Path

folder_path = Path("../../texts")

files = [
    p for p in folder_path.rglob("*")
    if p.is_file()
]

print(files[0])

loader = UnstructuredLoader(
    files[0],
    chunking_strategy="basic",
    max_characters=2000,
    include_orig_elements=False,
    post_processors=[clean_extra_whitespace],
)

docs = loader.load()

print("Number of LangChain documents:", len(docs))
print("Length of text in the document:", len(docs[0].page_content))