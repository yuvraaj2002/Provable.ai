from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class Verdict(str, Enum):
    """Simplified verdict options"""
    SUPPORTED = "SUPPORTED"
    NOT_SUPPORTED = "NOT_SUPPORTED"

class SimpleClaimVerdict(BaseModel):
    """Simple verdict for a single claim"""
    claim_text: str = Field(..., description="The claim being verified")
    verdict: Verdict = Field(..., description="SUPPORTED or NOT_SUPPORTED")
    reasoning: str = Field(..., description="Brief explanation")

class SimpleVerificationOutput(BaseModel):
    """Simple output for claim verification"""
    verdicts: List[SimpleClaimVerdict] = Field(..., description="List of claim verdicts")
    total_claims: int = Field(..., description="Total claims checked")
    supported_claims: int = Field(..., description="Number of supported claims")
    not_supported_claims: int = Field(..., description="Number of unsupported claims")