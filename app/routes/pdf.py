from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.analyzer import analyze_pdf
import os
import uuid


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadPDFResponse(BaseModel):
    id: str

class AskQuestionRequest(BaseModel):
    pdfId: str
    question: str

class AskQuestionResponse(BaseModel):
    answer: str
    confidence: float
    source: str

@router.post("/api/upload", response_model=UploadPDFResponse)
async def upload_pdf(file: UploadFile = File(...)):    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail={"code": "INVALID_FILE_TYPE", "message": "Only PDF files are allowed."})
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "UPLOAD_ERROR", "message": str(e)})

@router.post("/api/ask", response_model=AskQuestionResponse)
async def ask_question(req: AskQuestionRequest):
    if not req.pdfId:
        raise HTTPException(status_code=400, detail={"code": "MISSING_PDF_ID", "message": "PDF ID is required."})
    if not req.question or len(req.question.strip()) == 0:
        raise HTTPException(status_code=400, detail={"code": "INVALID_QUESTION", "message": "Question is required."})
    file_path = os.path.join(UPLOAD_DIR, f"{req.pdfId}.pdf")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail={"code": "MISSING_PDF_ID", "message": "PDF not found."})
    try:
        # Pass pdfId and question to analyze_pdf
        answer = analyze_pdf(file_path, pdf_id=req.pdfId, question=req.question)
        return {"answer": answer, "confidence": 1.0, "source": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "PROCESSING_ERROR", "message": str(e)})


