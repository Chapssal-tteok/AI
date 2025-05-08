from fastapi import APIRouter
from app.services.perplexity_service import query_perplexity
from app.models.search_model import PerplexityRequest, PerplexityResponse

router = APIRouter()

@router.post("/search", response_model=PerplexityResponse)
def search_perplexity(req: PerplexityRequest):
    result = query_perplexity(req.query)
    return PerplexityResponse(result=result)