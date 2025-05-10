# app/api/perplexity.py

from fastapi import APIRouter, Body
from app.services.perplexity_service import search_perplexity_summary
from pydantic import BaseModel

router = APIRouter()

class PerplexitySummaryRequest(BaseModel):
    query: str

class PerplexitySummaryResponse(BaseModel):
    summary: str

@router.post(
    "/summary",
    summary="기업/직무 요약 검색 (Perplexity)",
    description="기업 및 직무 정보를 기반으로 Perplexity API를 호출하여 핵심 내용을 요약해 반환합니다.",
    response_model=PerplexitySummaryResponse,
    responses={
        200: {
            "description": "요약 결과 반환",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "네이버는 대한민국의 대표적인 IT 기업으로, 다양한 온라인 플랫폼 서비스를 제공합니다. 백엔드 개발자는 서버 아키텍처 설계 및 대용량 트래픽 처리 시스템 개발을 담당합니다."
                    }
                }
            }
        }
    }
)
def get_perplexity_summary(req: PerplexitySummaryRequest = Body(..., example={
    "query": "네이버 백엔드 개발자"
})):
    summary = search_perplexity_summary(req.query)
    return PerplexitySummaryResponse(summary=summary)
