from fastapi import FastAPI
from app.routes import pdf

app = FastAPI()

app.include_router(pdf.router)

@app.get("/health")
def health():
    return {"status": "ok"}
