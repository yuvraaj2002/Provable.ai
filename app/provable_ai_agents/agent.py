from typing import Type

from app.core.config import settings
from pydantic import BaseModel
from openai import OpenAI


class CustomAgents:

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def run_agent(self, model: str, prompt: str, output_schema: Type[BaseModel]):
        """Run an agent using OpenAI responses API with structured output."""
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




