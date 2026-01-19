from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from lnagchain_core.documents import documents
from langchain_unstructured import UnstructuredLoader
import os

files = [""]

loader = UnstructuredLoader(
    file_paths,
    chunking_strategy="basic",
    max_characters=1000000,
    include_orig_elements=False,
    post_processors=[clean_extra_whitespace],)

docs = loader.load()

print("Number of LangChain documents:", len(docs))
print("Length of text in the document:", len(docs[0].page_content))