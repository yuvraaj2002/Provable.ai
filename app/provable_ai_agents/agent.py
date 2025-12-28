from app.core.config import settings
from pydantic import BaseModel
from openai import OpenAI

class CustomAgents():

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def run_agent(self, model: str, prompt: str, output_schema: BaseModel):
        """
        Run an agent using OpenAI responses API.
        
        Args:
            model: The model to use (e.g., "gpt-4o", "o1-preview")
            prompt: The input prompt for the agent
            output_schema: The response format schema (JSON schema format)
            
        Returns:
            Response object from OpenAI, or None if error occurs
        """
        try:
            response = self.openai_client.responses.parse(
                model=model,
                input=prompt,
                text_format=output_schema
            )
            return response
        except Exception as e:
            print(f"Error running agent: {e}")
            import traceback
            traceback.print_exc()
            return None




