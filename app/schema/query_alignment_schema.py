from pydantic import BaseModel, Field
from typing import List, Literal

class QueryAlignmentOutput(BaseModel):
    """Output schema for query-response alignment evaluation."""
    alignment_verdict: Literal["ALIGNED", "PARTIALLY_ALIGNED", "NOT_ALIGNED"] = Field(
        description="Overall alignment verdict between query and response"
    )
    relevance_score: float = Field(
        description="Score from 0.0 to 1.0 indicating how well the response addresses the query"
    )
    addressed_aspects: List[str] = Field(
        description="List of query aspects that were addressed in the response"
    )
    missing_aspects: List[str] = Field(
        description="List of query aspects that were NOT addressed in the response"
    )
    reasoning: str = Field(
        description="Detailed explanation of the alignment evaluation"
    )