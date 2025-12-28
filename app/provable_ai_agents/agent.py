from google.adk.agents.llm_agent import Agent
from app.core.config import settings

class CustomAgents():

    def __init__(self):
        pass

    def _load_prompt(self,prompt_path):
        try:
            pass
        except Exception as e:
            return None

    def create_agent(self, name:str, model:str, instruction_prompt_path:str, description:str, output_key:str):
        try:
            # Loading the prompt
            instruction_prompt_md = self._load_prompt(instruction_prompt_path)
            if instruction_prompt_md is None:
                return None
            
            # Instantiating the Agent
            agent = Agent(
                name=name,
                model=model,
                instruction=instruction_prompt_md,
                description=description,
                output_key=output_key
            )
            return agent
        except Exception as e:
            return None




