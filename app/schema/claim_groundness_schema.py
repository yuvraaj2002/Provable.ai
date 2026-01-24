from pydantic import BaseModel, Field
from typing import List, Literal

class ClaimVerdict(BaseModel):
    claim_text: str = Field(description="The exact claim text being verified")
    verdict: Literal["SUPPORTED", "NOT_SUPPORTED"] = Field(description="The final verdict")
    reasoning: str = Field(description="Brief explanation of why you chose this verdict")

class SimpleVerificationOutput(BaseModel):
    verdicts: List[ClaimVerdict]
    total_claims: int
    supported_claims: int
    not_supported_claims: int