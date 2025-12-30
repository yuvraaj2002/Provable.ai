from app.provable_ai_agents.agent import CustomAgents
from app.schema.claim_extraction_schema import ClaimExtractionOutput
from app.schema.context_utilization_schema import ContextUtilizationOutput
from app.provable_ai_agents.prompts import CLAIM_EXTRACTOR_SYSTEM_PROMPT, CLAIM_VERIFICATION_SYSTEM_PROMPT, CONTEXT_UTILIZATION_SYSTEM_PROMPT
from app.helpers.generator_quality_evaluation_helper import GeneratorQualityEvaluationHelper
from rich import print
from concurrent.futures import ThreadPoolExecutor

class LLMService():
    def __init__(self):
        self.agent_creator = CustomAgents()
        self.helper = GeneratorQualityEvaluationHelper()

    async def evaluate_generator(self, input_data):
        """
        Analyzes faithfulness by:
        1. Extracting claims from the LLM response
        2. Getting context utilization (which chunks were used)
        Both operations run in parallel using ThreadPoolExecutor
        
        Args:
            input_data: EvaluateGeneratorRequest containing query, context, and llm_response
            
        Returns:
            dict with extraction results including claims and context utilization
        """
        try:
            # Format chunks for context utilization prompt
            formatted_chunks = self.helper._format_chunks_for_utilization(input_data.context_retrieved)
            
            # Format prompts for both agents
            formatted_claim_extraction_prompt = CLAIM_EXTRACTOR_SYSTEM_PROMPT.format(
                llm_response=input_data.llm_response
            )
            formatted_chunk_utilization_prompt = CONTEXT_UTILIZATION_SYSTEM_PROMPT.format(
                llm_response=input_data.llm_response,
                chunks=formatted_chunks
            )
            
            # Define functions to run agents
            def run_claim_extraction():
                return self.agent_creator.run_agent(
                    model="gpt-4.1",
                    prompt=formatted_claim_extraction_prompt,
                    output_schema=ClaimExtractionOutput
                )
            
            def run_context_utilization():
                return self.agent_creator.run_agent(
                    model="gpt-4.1",
                    prompt=formatted_chunk_utilization_prompt,
                    output_schema=ContextUtilizationOutput,
                )
            
            # Execute both agents in parallel using ThreadPoolExecutor with 2 threads
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both tasks
                claim_future = executor.submit(run_claim_extraction)
                utilization_future = executor.submit(run_context_utilization)
                
                # Wait for both to complete and get results
                claim_response = claim_future.result()
                utilization_response = utilization_future.result()
            
            # Extract outputs
            extracted_claims = self.helper.extract_claim_extraction_output(claim_response)
            context_utilization = self.helper.extract_context_utilization_output(utilization_response)
            
            # Build response dictionary
            result = {}
            
            if extracted_claims:
                result['claims'] = extracted_claims.model_dump()
            else:
                result['claims'] = None
            
            if context_utilization:
                result['context_utilization'] = context_utilization.model_dump()
            else:
                result['context_utilization'] = None
            
            return result

        except Exception as e:
            print(f"Error in evaluate_generator: {e}")
            import traceback
            traceback.print_exc()
            return None