# app/api/interview/route.py

from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Dict
from app.services.chroma_service import search_similar_questions
from app.services.gpt_service import get_chat_response
from app.services.perplexity_service import search_perplexity_summary
from app.prompts.resume_analyze_prompts import generate_resume_analysis_prompt
from app.prompts.analyze_answer_prompts import analyze_answer_prompt
from app.prompts.follow_up_prompts import generate_follow_up_prompt
from app.prompts.interview_qas_prompts import generate_interview_qas_prompt

router = APIRouter()

class ResumeRequest(BaseModel):
    resume: str
    company: str
    position: str

class AnswerAnalysisRequest(BaseModel):
    question: str
    answer: str
    resume: str

class FollowUpRequest(BaseModel):
    question: str
    answer: str

class InterviewQasRequest(BaseModel):
    company: str
    position: str
    resumeContent: str

@router.post(
    "/analyze-resume",
    summary="자기소개서 분석",
    description="자기소개서와 지원 정보(기업, 직무)를 바탕으로 피드백을 제공합니다.",
    response_model=Dict[str, List[str]],
    responses={
        200: {
            "description": "분석된 피드백 목록 반환",
            "content": {
                "application/json": {
                    "example": {
                        "feedback": [
                            "**논리적 흐름**: 자기소개서의 전체 흐름이 부드럽고 자연스러워요.",
                            "**구체성**: 경험이 구체적으로 잘 드러나 있어 설득력이 높아요.",
                            "**개선 포인트**: 두 번째 문단의 예시는 다소 모호하니 구체적인 수치나 결과를 추가해보세요."
                        ]
                    }
                }
            }
        }
    }
)
async def analyze_resume(req: ResumeRequest = Body(..., example={
    "resume": "저는 대학 생활 동안 다양한 팀 프로젝트를 수행하며 협업 능력을 키웠습니다...",
    "company": "네이버",
    "position": "백엔드 개발자"
})):
    prompt = generate_resume_analysis_prompt(req.resume, req.company, req.position)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "분석 실패"}

    feedback = [line for line in response.split("\n") if line.strip()]
    return {"feedback": feedback}

@router.post(
    "/analyze-answer",
    summary="면접 답변 분석",
    description="면접 질문과 답변, 자기소개서를 기반으로 답변의 강점, 약점, 개선 포인트 등을 분석합니다.",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "답변 분석 결과 반환",
            "content": {
                "application/json": {
                    "example": {
                        "analysis": "1. 강점: 질문 의도를 잘 파악하고 경험을 구체적으로 서술함..."
                    }
                }
            }
        }
    }
)
async def analyze_answer(req: AnswerAnalysisRequest = Body(..., example={
    "question": "어려운 상황에서 갈등을 해결한 경험이 있나요?",
    "answer": "저는 동아리 프로젝트에서 일정이 지연된 팀원과 갈등을 겪은 적 있습니다...",
    "resume": "저는 다양한 협업 프로젝트를 통해 갈등 조정 능력을 키웠습니다..."
})):
    prompt = analyze_answer_prompt(req.question, req.answer, req.resume)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "답변 분석 실패"}

    return {"analysis": response}

@router.post(
    "/follow-up",
    summary="추가 면접 질문 생성",
    description="지원자의 답변을 바탕으로 더 깊이 있는 추가 면접 질문을 생성합니다.",
    response_model=Dict[str, List[str]],
    responses={
        200: {
            "description": "추가 질문 목록 반환",
            "content": {
                "application/json": {
                    "example": {
                        "followUps": ["당시 팀원과의 갈등을 해결한 과정에서 가장 어려웠던 점은 무엇인가요?"]
                    }
                }
            }
        }
    }
)
async def generate_follow_up(req: FollowUpRequest = Body(..., example={
    "question": "갈등을 해결한 경험이 있나요?",
    "answer": "네, 저는 프로젝트에서..."
})):
    prompt = generate_follow_up_prompt(req.question, req.answer)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "추가 질문 생성 실패"}

    follow_ups = [line for line in response.split("\n") if line.strip()]
    return {"followUps": follow_ups}

@router.post(
    "/generate-qas",
    summary="면접 질문 생성",
    description="기업과 직무 정보, 자기소개서를 기반으로 예상 면접 질문을 생성합니다.",
    response_model=Dict[str, List[str]],
    responses={
        200: {
            "description": "생성된 면접 질문 목록 반환",
            "content": {
                "application/json": {
                    "example": {
                        "questions": [
                            "[네이버] 백엔드 개발자로서 최근 프로젝트 중 가장 도전적이었던 경험은 무엇인가요?",
                            "자신의 기술 스택 중 네이버에서 가장 잘 활용할 수 있는 역량은 무엇이라고 생각하나요?"
                        ]
                    }
                }
            }
        }
    }
)
async def generate_interview_questions(req: InterviewQasRequest = Body(..., example={
    "company": "네이버",
    "position": "백엔드 개발자",
    "resumeContent": "저는 대규모 트래픽 처리를 위한 백엔드 시스템 설계를 경험했습니다..."
})):
    # 1. 기업 + 직무로 Perplexity 요약 검색
    search_query = f"{req.company} {req.position}"
    pplx_summary = search_perplexity_summary(search_query)

    # 2. Chroma에서 기업, 직무 관련 질문 가져오기
    company_questions = search_similar_questions(req.company)
    position_questions = search_similar_questions(req.position)

    company_q_text = "\n".join([q["content"] for q in company_questions])
    position_q_text = "\n".join([q["content"] for q in position_questions])

    chroma_examples = f"[기업: {req.company}] 관련 질문들:\n{company_q_text}\n\n[직무: {req.position}] 관련 질문들:\n{position_q_text}"

    # 3. 요약 결과와 자기소개서 내용을 합쳐 프롬프트 생성
    prompt = generate_interview_qas_prompt(pplx_summary, req.resumeContent, chroma_examples)
    
    # 4. GPT로 질문 생성
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "질문 생성 실패"}

    questions = [line for line in response.split("\n") if line.strip()]
    return {"questions": questions}
