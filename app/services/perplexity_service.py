# app/services/perplexity_service.py

import requests
from app.core.config import settings

def query_perplexity(query: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}"
    }
    response = requests.post(
        "https://api.perplexity.ai/search",
        headers=headers,
        json={"query": query}
    )
    return response.json().get("result", "No result")