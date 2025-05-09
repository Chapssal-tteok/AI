# app/services/perplexity_service.py

import os
import requests
from dotenv import load_dotenv

# .env 로드
load_dotenv()

PPLX_API_KEY = os.getenv("PPLX_API_KEY")

def search_perplexity_summary(query: str) -> str:
    """
    Perplexity API를 이용하여 기업과 직무 관련 요약 정보를 가져옵니다.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PPLX_API_KEY}",
    }

    messages = [
        {
            "role": "system",
            "content": (
                "당신은 전문적인 리서치 어시스턴트입니다. "
                "사용자의 질의에 대해 핵심적인 기업 및 직무 개요를 짧고 간결하게 정리해 주세요."
            ),
        },
        {
            "role": "user",
            "content": f"{query}에 대한 개요를 알려줘. 기업 개요와 직무의 특징을 중심으로 요약해줘.",
        },
    ]

    payload = {
        "model": "sonar",
        "messages": messages,
        "max_tokens": 700,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"❌ Perplexity API 호출 실패: {e}")
        return "Perplexity 검색 실패"
