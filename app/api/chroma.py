# app/api/chroma.py

from fastapi import APIRouter
from app.services.chroma_service import search_similar_questions
from app.models.search_model import ChromaRequest, ChromaResponse

router = APIRouter()

@router.post("/search", response_model=ChromaResponse)
def search_chroma(req: ChromaRequest):
    result = search_similar_questions(req.query)
    return ChromaResponse(results=result)