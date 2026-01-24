from pydantic import BaseModel, Field
from typing import List

class ClaimExtractionOutput(BaseModel):
    """A collection of independent factual claims extracted from a text."""
    claims: List[str] = Field(description="A list of standalone, atomic factual statements.")