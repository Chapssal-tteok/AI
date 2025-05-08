from fastapi import APIRouter
from app.services.gpt_service import prompt_gpt
from app.models.search_model import GPTRequest, GPTResponse

router = APIRouter()

@router.post("/chat", response_model=GPTResponse)
def chat_with_gpt(request: GPTRequest):
    result = prompt_gpt(request.prompt)
    return GPTResponse(answer=result)