# main.py

from fastapi import FastAPI
from app.api import perplexity, chroma
from app.api.interview import route as interview_route

app = FastAPI()

app.include_router(perplexity.router, prefix="/perplexity")
app.include_router(chroma.router, prefix="/chroma")
app.include_router(interview_route.router, prefix="/interview")