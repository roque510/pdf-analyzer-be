from fastapi import FastAPI
from app.routes import pdf
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
import os

app = FastAPI()

app.include_router(pdf.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
DELETE_AFTER_SECONDS = 3600  # 1 hour

def cleanup_uploads():
    while True:
        now = time.time()
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                if now - os.path.getmtime(file_path) > DELETE_AFTER_SECONDS:
                    os.remove(file_path)
        time.sleep(300)  # Check every 5 minutes

threading.Thread(target=cleanup_uploads, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return {"status": "ok", "message": "Service is running"}
