from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_unstructured import UnstructuredLoader
from langchain_core.prompts import PromptTemplate
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

retriever = db.as_retriever(search_kwargs={"k": 4})

prompt = PromptTemplate(
    template="""
You are a helpful assistant.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"],
)

llm = ChatOllama(model="llama3")

qa_chain = prompt | llm

query = "tell me about emperor of mankind"

docs = retriever.get_relevant_documents(query)

context = "\n\n".join([d.page_content for d in docs])

answer = qa_chain.run({"context": context, "question": query})
print(answer)

