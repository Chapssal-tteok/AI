# main.py
from fastapi import FastAPI
from app.api import gpt, perplexity, chroma

app = FastAPI()

app.include_router(gpt.router, prefix="/gpt")
app.include_router(perplexity.router, prefix="/perplexity")
app.include_router(chroma.router, prefix="/chroma")