# app/api/interview/route.py

from fastapi import APIRouter
from pydantic import BaseModel
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


@router.post("/analyze-resume")
async def analyze_resume(req: ResumeRequest):
    prompt = generate_resume_analysis_prompt(req.resume, req.company, req.position)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "분석 실패"}

    feedback = [line for line in response.split("\n") if line.strip()]
    return {"feedback": feedback}


@router.post("/analyze-answer")
async def analyze_answer(req: AnswerAnalysisRequest):
    prompt = analyze_answer_prompt(req.question, req.answer, req.resume)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "답변 분석 실패"}

    return {"analysis": response}


@router.post("/follow-up")
async def generate_follow_up(req: FollowUpRequest):
    prompt = generate_follow_up_prompt(req.question, req.answer)
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "후속 질문 생성 실패"}

    follow_ups = [line for line in response.split("\n") if line.strip()]
    return {"followUps": follow_ups}


@router.post("/generate-qas")
async def generate_interview_questions(req: InterviewQasRequest):
    # 1. 기업 + 직무로 Perplexity 요약 검색
    search_query = f"{req.company} {req.position}"
    pplx_summary = search_perplexity_summary(search_query)

    # 2. 요약 결과와 자기소개서 내용을 합쳐 프롬프트 생성
    prompt = generate_interview_qas_prompt(pplx_summary, req.resumeContent)

    print("📨 최종 prompt:\n", prompt)
    print("📏 길이:", len(prompt))
    
    # 3. GPT로 질문 생성
    response = get_chat_response(prompt, model="sonar", mode="text")

    if not response or not isinstance(response, str):
        return {"message": "질문 생성 실패"}

    questions = [line for line in response.split("\n") if line.strip()]
    return {"questions": questions}
