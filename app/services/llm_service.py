from app.provable_ai_agents.agent import CustomAgents
from typing import Optional
from app.schema.claim_extraction_schema import ClaimExtractionOutput
from app.schema.claim_verification_schema import SimpleVerificationOutput
from app.provable_ai_agents.prompts.claims_extraction_prompt import CLAIM_EXTRACTOR_SYSTEM_PROMPT
from app.provable_ai_agents.prompts.claim_verification_prompt import CLAIM_VERIFICATION_SYSTEM_PROMPT
import json
from rich import print

class LLMService():
    def __init__(self):
        self.agent_creator = CustomAgents()

    def extract_claim_extraction_output(self, response) -> Optional[ClaimExtractionOutput]:
        """Clean extraction of parsed ClaimExtractionOutput from OpenAI Responses API."""
        if not response or not response.output:
            return None
        message = response.output[0]
        if not message.content:
            return None
        content = message.content[0]
        if hasattr(content, "parsed"):
            return content.parsed 
        return None

    def extract_verification_output(self, response) -> Optional[SimpleVerificationOutput]:
        """Clean extraction of parsed SimpleVerificationOutput from OpenAI Responses API."""
        if not response or not response.output:
            return None
        message = response.output[0]
        if not message.content:
            return None
        content = message.content[0]
        if hasattr(content, "parsed"):
            return content.parsed 
        return None

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

    def calculate_faithfulness_score(self,total_claims: int, supported_claims: int) -> float:
        if total_claims == 0:
            return 1.0  # No claims = technically faithful
        
        return supported_claims / total_claims

    async def analyze_faithfulness(self, input_data):
        """
        Analyzes faithfulness by:
        1. Extracting claims from the LLM response
        2. Verifying each claim against the provided context
        
        Args:
            input_data: EvaluateFaithfulnessRequest containing query, context, and llm_response
            
        Returns:
            dict with verification results including verdicts, scores, and claims
        """
        try:
            # Step 1: Extract claims from LLM response
            formatted_extraction_prompt = CLAIM_EXTRACTOR_SYSTEM_PROMPT.format(
                llm_response=input_data.llm_response
            )
            
            extraction_response = self.agent_creator.run_agent(
                model="gpt-4.1",  
                prompt=formatted_extraction_prompt,
                output_schema=ClaimExtractionOutput
            )
            
            extracted_claims = self.extract_claim_extraction_output(extraction_response)
            if extracted_claims is None or not extracted_claims.claims:
                return None
            
            # Step 2: Format context and claims for verification
            formatted_context = self._format_context(input_data.context_retrieved)
            formatted_claims = self._format_claims_for_verification(extracted_claims.claims)
            
            # Step 3: Verify claims against context
            # Update prompt to handle multiple claims
            verification_prompt_template = CLAIM_VERIFICATION_SYSTEM_PROMPT.replace(
                "CLAIM TO VERIFY:\n{claim}",
                "CLAIMS TO VERIFY:\n{claim}\n\nEvaluate EACH claim above against the context. Provide verdicts for ALL claims in the list."
            )
            
            formatted_verification_prompt = verification_prompt_template.format(
                context=formatted_context,
                claim=formatted_claims
            )
            
            verification_response = self.agent_creator.run_agent(
                model="gpt-4.1",
                prompt=formatted_verification_prompt,
                output_schema=SimpleVerificationOutput
            )
            
            verification_output = self.extract_verification_output(verification_response)
            if verification_output is None:
                return None
            
            # Return the verification results as dict
            response_dict = verification_output.model_dump()
            response_dict['faithfullness_score'] = self.calculate_faithfulness_score(response_dict['total_claims'],response_dict['supported_claims'])
            return response_dict

        except Exception as e:
            print(f"Error in analyze_faithfulness: {e}")
            import traceback
            traceback.print_exc()
            return None