from app.provable_ai_agents.states import GeneratorEvaluationState
from app.provable_ai_agents.prompts import CLAIM_VERIFICATION_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from app.schema import SimpleVerificationOutput
from app.provable_ai_agents.tools import ComputeGroundness
from app.core.config import settings
import textwrap

def groundness_evaluation_node(state:GeneratorEvaluationState) -> GeneratorEvaluationState:

    # Getting the atomic claims and context chunks from state
    atomic_claims = state["atomic_claims"]
    context_chunks = state["context_chunks"]

    # If no claims exist, we can't evaluate
    if not atomic_claims:
        return {"groundness_results": {"score": 0, "error": "No claims found"}}

    # If no context chunks exist, we can't evaluate
    if not context_chunks:
        return {"groundness_results": {"score": 0, "error": "No context chunks found"}}

    # Formatting the context chunks and atomic claims for the prompt
    context_text = "\n\n".join(context_chunks)
    claims_text = "\n".join(atomic_claims)

    # Formatting the prompt
    formatted_prompt = textwrap.dedent(CLAIM_VERIFICATION_SYSTEM_PROMPT).format(context=context_text, claim=claims_text)

    # Setting up the LLM (Brain)
    model = init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        api_key=settings.GEMINI_KEY,
    )

    # Attaching the structured schema with llm
    model_with_structured_output = model.with_structured_output(SimpleVerificationOutput)

    # Making the LLM call
    groundness_analysis = model_with_structured_output.invoke(formatted_prompt)

    # Calling the compute_groundness_score function
    groundness_score = ComputeGroundness.compute_groundness_score(groundness_analysis.total_claims, groundness_analysis.supported_claims)

    # Return only the updated keys for LangGraph
    return {"groundness_results": {"score": groundness_score, "groundness_analysis": groundness_analysis}}