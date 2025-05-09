# app/api/perplexity.py

from fastapi import APIRouter
from app.services.perplexity_service import search_perplexity_summary
from pydantic import BaseModel

router = APIRouter()

class PerplexitySummaryRequest(BaseModel):
    query: str

class PerplexitySummaryResponse(BaseModel):
    summary: str

@router.post("/summary", response_model=PerplexitySummaryResponse)
def get_perplexity_summary(req: PerplexitySummaryRequest):
    summary = search_perplexity_summary(req.query)
    return PerplexitySummaryResponse(summary=summary)
