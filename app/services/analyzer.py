from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
model = os.getenv("OLLAMA_MODEL", "llama3")

def analyze_pdf(path: str) -> str:
    loader = PyPDFLoader(path)
    docs = loader.load()
    embeddings = OllamaEmbeddings(model=model)
    db = Chroma.from_documents(docs, embeddings, persist_directory="index")
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=embeddings.client, retriever=retriever)
    return qa.run("Summarize this document.")
