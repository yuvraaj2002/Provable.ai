from typing import Dict
from pydantic import BaseModel, Field

class PIIQuestionGeneratorOutput(BaseModel):
    """Output format for the PII Question Generator Agent"""
    questions: Dict[str, str] = Field(
        ..., 
        description="Dictionary where keys are question numbers (as strings) and values are the question content"
    )
    
    def get_questions_list(self) -> list:
        """Helper method to get questions as a list in order"""
        return [self.questions[str(i)] for i in range(1, len(self.questions) + 1)]

