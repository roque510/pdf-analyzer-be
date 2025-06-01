from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
from langchain_community.llms import Ollama

load_dotenv()
model = os.getenv("OLLAMA_MODEL", "llama3")

def analyze_pdf(path: str, pdf_id: str = None, question: str = "Summarize this document.") -> str:
    loader = PyPDFLoader(path)
    docs = loader.load()
    embeddings = OllamaEmbeddings(model=model)
    persist_dir = f"index/{pdf_id}" if pdf_id else "index"
    os.makedirs(persist_dir, exist_ok=True)
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    retriever = db.as_retriever()
    llm = Ollama(model=model)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)
