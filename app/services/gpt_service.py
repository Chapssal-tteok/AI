import openai
from app.core.config import settings

def prompt_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        api_key=settings.OPENAI_API_KEY
    )
    return response['choices'][0]['message']['content']