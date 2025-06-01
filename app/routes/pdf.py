from fastapi import APIRouter, File, UploadFile, Form
from app.services.analyzer import analyze_pdf
import os

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join("uploads", file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    result = analyze_pdf(path)
    return {"answer": result}
