from typing import List, Optional, Type
from pydantic import BaseModel
import numpy as np
from app.schema.claim_extraction_schema import ClaimExtractionOutput
from app.schema.claim_verification_schema import SimpleVerificationOutput
from app.schema.context_utilization_schema import ChunkUtilization, ContextUtilizationOutput


class GeneratorQualityEvaluationHelper:

    def __init__(self):
        pass

    def _parse_response(self, response, model_class: Type[BaseModel]) -> Optional[BaseModel]:
        """Parse OpenAI response into the provided Pydantic model."""
        if not response or not response.output:
            return None
        message = response.output[0]
        if not message.content:
            return None
        content = message.content[0]
        parsed = getattr(content, "parsed", None)
        if parsed is None:
            return None
        if isinstance(parsed, dict):
            return model_class.model_validate(parsed)
        if isinstance(parsed, BaseModel):
            return parsed
        return None

    def extract_claim_extraction_output(self, response) -> Optional[ClaimExtractionOutput]:
        return self._parse_response(response, ClaimExtractionOutput)

    def extract_verification_output(self, response) -> Optional[SimpleVerificationOutput]:
        return self._parse_response(response, SimpleVerificationOutput)

    def extract_context_utilization_output(self, response) -> Optional[ContextUtilizationOutput]:
        return self._parse_response(response, ContextUtilizationOutput)

    def _format_context(self, context_retrieved):
        """Format context chunks into a single string."""
        context_parts = []
        for chunk_id, chunk in context_retrieved.items():
            context_parts.append(f"[Chunk {chunk_id}]: {chunk.content}")
        return "\n\n".join(context_parts)

    def _format_claims_for_verification(self, claims):
        """Format claims list into a string for the verification prompt."""
        claims_list = []
        for i, claim in enumerate(claims, 1):
            claims_list.append(f"{i}. {claim.claim_text}")
        return "\n".join(claims_list)

    def _format_chunks_for_utilization(self, context_retrieved):
        """Format context chunks into a string for the context utilization prompt."""
        chunk_parts = []
        for chunk_id, chunk in context_retrieved.items():
            chunk_parts.append(f"{chunk_id} : {chunk.content}")
        return "\n\n".join(chunk_parts)

    def calculate_faithfulness_score(self, total_claims: int, supported_claims: int) -> float:
        """Calculate faithfulness score based on supported claims."""
        if total_claims == 0:
            return 1.0  # No claims = technically faithful
        
        return supported_claims / total_claims

    def calculate_context_utilization(self, chunks: List[ChunkUtilization]) -> float:
        """Calculates context utilization using Average Precision over chunk usage."""
        if not chunks:
            return 0.0

        relevant_count = 0
        precision_values = []

        for i, chunk in enumerate(chunks):
            if chunk.utilized == 1:
                relevant_count += 1
            precision_values.append(relevant_count / (i + 1))

        return float(np.mean(precision_values))
