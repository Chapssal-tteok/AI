# app/api/chroma.py

from fastapi import APIRouter, Body
from app.services.chroma_service import search_similar_questions
from app.models.search_model import ChromaRequest, ChromaResponse

router = APIRouter()

@router.post(
    "/search",
    summary="유사 질문 검색",
    description="질문을 입력하면 Chroma DB를 통해 유사한 질문 3개를 검색하여 반환합니다.",
    response_model=ChromaResponse,
    responses={
        200: {
            "description": "유사 질문 목록 반환",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "content": "팀 프로젝트 중 갈등을 해결한 경험에 대해 말씀해 주세요.",
                                "metadata": {"source": "faq_dataset_001"}
                            },
                            {
                                "content": "협업 중 마찰을 겪었던 사례를 말해주세요.",
                                "metadata": {"source": "faq_dataset_002"}
                            },
                            {
                                "content": "조직 내 갈등 상황에서 본인이 한 역할은 무엇인가요?",
                                "metadata": {"source": "faq_dataset_003"}
                            }
                        ]
                    }
                }
            }
        }
    }
)
def search_chroma(req: ChromaRequest = Body(..., example={
    "query": "갈등을 해결한 경험이 있나요?"
})):
    result = search_similar_questions(req.query)
    return ChromaResponse(results=result)