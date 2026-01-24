import textwrap
from app.core.config import settings
from app.provable_ai_agents.states import GeneratorEvaluationState
from app.provable_ai_agents.prompts import CLAIM_EXTRACTOR_SYSTEM_PROMPT
from app.schema import ClaimExtractionOutput
from langchain.chat_models import init_chat_model

def claim_extractor_node(state:GeneratorEvaluationState) -> GeneratorEvaluationState:

    # Extracting the llm_response from the state
    llm_response = state["llm_response"]

    # Formatting the prompt
    formatted_prompt = textwrap.dedent(CLAIM_EXTRACTOR_SYSTEM_PROMPT).format(llm_response=llm_response)

    # Setting up the LLM (Brain)
    model = init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        api_key=settings.GEMINI_KEY,
    )

    # Connecting the schema with the model
    model_with_structure = model.with_structured_output(ClaimExtractionOutput)

    # Executing the model
    response = model_with_structure.invoke(formatted_prompt)

    # Return only the updated keys for LangGraph
    return {"atomic_claims": response.claims}