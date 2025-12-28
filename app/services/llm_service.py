from app.provable_ai_agents.agent import CustomAgents
from typing import Optional
from app.schema.claim_extraction_schema import ClaimExtractionOutput
from app.provable_ai_agents.prompts.claims_extraction_prompt import CLAIM_EXTRACTOR_SYSTEM_PROMPT
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

    async def analyze_faithfulness(self, input_data):
        """
        Analyzes faithfulness by extracting claims from the LLM response using OpenAI responses API.
        
        Args:
            input_data: EvaluateFaithfulnessRequest containing query, context, and llm_response
            
        Returns:
            dict with claims and total_claims
        """
        try:
            # Format the prompt with the actual LLM response
            formatted_prompt = CLAIM_EXTRACTOR_SYSTEM_PROMPT.format(
                llm_response=input_data.llm_response
            )
            
            # Run the agent using OpenAI responses API
            response = self.agent_creator.run_agent(
                model="gpt-4.1",  
                prompt=formatted_prompt,
                output_schema=ClaimExtractionOutput
            )
            parsed_output = self.extract_claim_extraction_output(response)
            if parsed_output is None:
                return None
            return parsed_output.model_dump()

        except Exception as e:
            print(f"Error in analyze_faithfulness: {e}")
            import traceback
            traceback.print_exc()
            return None