from typing import List, Literal
from pydantic import BaseModel, Field


class ChunkRelevance(BaseModel):
    chunk_id: str = Field(..., description="The chunk identifier")
    relevant: Literal[0, 1] = Field(..., description="0 = not relevant, 1 = relevant")


class ChunkRelevanceOutput(BaseModel):
    chunks: List[ChunkRelevance] = Field(..., description="Relevance status for each chunk")

