# app/models/search_model.py

from pydantic import BaseModel
from typing import List, Dict

class PerplexityRequest(BaseModel):
    query: str

class PerplexityResponse(BaseModel):
    result: str

class ChromaRequest(BaseModel):
    query: str

class ChromaResult(BaseModel):
    content: str
    metadata: Dict[str, str]

class ChromaResponse(BaseModel):
    results: List[ChromaResult]