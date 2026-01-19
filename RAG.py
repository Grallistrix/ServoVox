from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_unstructured import UnstructuredLoader
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores.utils import filter_complex_metadata
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
    files[0],
    chunking_strategy="basic",
    max_characters=2000,
    include_orig_elements=False,
   )

docs = loader.load()

print("Number of LangChain documents:", len(docs))
print("Length of text in the document:", len(docs[0].page_content))

clean_docs = filter_complex_metadata(docs)

embeddings = OllamaEmbeddings(model="twine/mxbai-embed-xsmall-v1")

print("Number of LangChain documents:", len(clean_docs))
print("Length of text in the document:", len(clean_docs[0].page_content))

db = Chroma.from_documents(
    clean_docs,
    embeddings,
    persist_directory="./chroma_db"
)

print("Total vectors:", db._collection.count())

results = db._collection.get(
    include=["documents", "metadatas", "ids"]
)

print(results)

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

docs = retriever.invoke(query)

context = "\n\n".join([d.page_content for d in docs])

for d in docs:
    print(d.page_content)

answer = qa_chain.invoke({"context": context, "question": query})
print(answer)

