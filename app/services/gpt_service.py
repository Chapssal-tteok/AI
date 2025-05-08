# app/services/gpt_service.py

import os
import requests
from dotenv import load_dotenv

# .env 로드
load_dotenv()

PPLX_API_KEY = os.getenv("PPLX_API_KEY")

def get_chat_response(prompt: str, model: str = "sonar", mode: str = "text") -> str | None:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PPLX_API_KEY}"
    }

    messages = [
        {
            "role": "system",
            "content": (
                "당신은 자기소개서를 분석해 피드백을 제공하고, "
                "면접 질문의 답변을 분석하며, 추가 질문을 제공하는 취업 컨설팅 전문가입니다. "
                "구체적이고 실질적인 피드백을 제공해주세요."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False
    }

    if mode == "json":
        payload["response_format"] = "json"

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ GPT API 호출 오류:", e)
        return None
