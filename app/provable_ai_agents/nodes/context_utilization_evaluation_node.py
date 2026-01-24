from app.provable_ai_agents.states import GeneratorEvaluationState
from app.provable_ai_agents.prompts import CONTEXT_UTILIZATION_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from app.schema import ContextUtilizationOutput
from app.provable_ai_agents.tools import ComputeChunkUtilizationScore
from app.core.config import settings
import textwrap

def context_utilization_evaluation_node(state:GeneratorEvaluationState) -> GeneratorEvaluationState:

    # Getting the llm response and context chunks from state
    llm_response = state["llm_response"]
    context_chunks = state["context_chunks"]

    # Formatting the prompt
    formatted_prompt = textwrap.dedent(CONTEXT_UTILIZATION_SYSTEM_PROMPT).format(llm_response=llm_response, chunks=context_chunks)

    # Setting up the LLM (Brain)
    model = init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        api_key=settings.GEMINI_KEY,
    )

    # Attaching the structured schema with llm
    model_with_structured_output = model.with_structured_output(ContextUtilizationOutput)

    # Making the LLM call
    context_utilization_analysis = model_with_structured_output.invoke(formatted_prompt)

    # Calling the compute_chunk_utilization_score function
    context_utilization_score = ComputeChunkUtilizationScore.compute_chunk_utilization_score(context_utilization_analysis.total_utilized_chunks, context_utilization_analysis.total_initialized_chunks)

    # Return only the updated keys for LangGraph
    return {
        "utilization_results": {
            "score": context_utilization_score,
            "context_utilization_analysis": context_utilization_analysis,
        }
    }