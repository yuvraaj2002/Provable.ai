from pydantic import BaseModel, Field
from typing import List, Literal

class ChunkUtilization(BaseModel):
    chunk_id: str = Field(description="The unique identifier or index of the context chunk")
    utilized: Literal[0, 1] = Field(description="1 if the chunk was used in the response, 0 otherwise")
    reasoning: str = Field(description="Brief explanation of why this chunk is considered utilized or not")

class ContextUtilizationOutput(BaseModel):
    chunks: List[ChunkUtilization]
    total_utilized_chunks: int = Field(description="Count of chunks with utilized=1")
    total_initialized_chunks: int = Field(description="Total number of chunks provided for analysis")
    chunk_utilization_score: float = Field(description="Score calculated as utilized / total")