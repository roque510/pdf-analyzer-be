from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "ollama" or "openai"
print("LLM_PROVIDER:", LLM_PROVIDER)
LLM_API_BASE = os.getenv("LLM_API_BASE")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_pdf(path: str, pdf_id: str = None, question: str = "Summarize this document.") -> str:
    loader = PyPDFLoader(path)
    docs = loader.load()
    persist_dir = f"index/{pdf_id}" if pdf_id else "index"
    os.makedirs(persist_dir, exist_ok=True)

    if LLM_PROVIDER == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings
        from langchain_community.llms import Ollama
        embeddings = OllamaEmbeddings(model=OLLAMA_MODEL, base_url=LLM_API_BASE) if LLM_API_BASE else OllamaEmbeddings(model=OLLAMA_MODEL)
        llm = Ollama(model=OLLAMA_MODEL, base_url=LLM_API_BASE) if LLM_API_BASE else Ollama(model=OLLAMA_MODEL)
    elif LLM_PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, openai_api_base=LLM_API_BASE) if LLM_API_BASE else OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, openai_api_base=LLM_API_BASE) if LLM_API_BASE else ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    else:
        raise ValueError("Unknown LLM_PROVIDER")

    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)
