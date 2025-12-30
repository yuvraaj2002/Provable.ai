from pydantic import BaseModel, Field
from typing import Dict

class ContextChunk(BaseModel):
    """Simple model for a retrieved context chunk"""
    content: str = Field(...)
    chunk_id: str = Field(...)
    score: float = Field(..., ge=0.0, le=1.0)

class EvaluateGeneratorRequest(BaseModel):
    """Simple request model for evaluation of the Generator part of the RAG architecture"""
    query: str = Field(..., min_length=1)
    context_retrieved: Dict[str, ContextChunk] = Field(...)
    llm_response: str = Field(..., min_length=1)