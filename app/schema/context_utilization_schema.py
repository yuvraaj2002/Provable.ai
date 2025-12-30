from typing import List, Literal
from pydantic import BaseModel, Field


class ChunkUtilization(BaseModel):
    chunk_id: str = Field(..., description="The chunk identifier")
    utilized: Literal[0, 1] = Field(..., description="0 = not utilized, 1 = utilized")


class ContextUtilizationOutput(BaseModel):
    chunks: List[ChunkUtilization] = Field(..., description="Utilization status for each chunk")
