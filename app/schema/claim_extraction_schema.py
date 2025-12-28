from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ExtractedClaim(BaseModel):
    claim_text: str = Field(..., description="The atomic claim extracted from the response")

class ClaimExtractionOutput(BaseModel):
    """Output format for the Claim Extractor Agent"""
    claims: List[ExtractedClaim] = Field(..., description="List of extracted atomic claims")
    total_claims: int = Field(..., description="Total number of claims extracted")