from app.provable_ai_agents.prompts import QUERY_ALIGNMENT_SYSTEM_PROMPT
from app.schema import QueryAlignmentOutput
from langchain.chat_models import init_chat_model
from app.provable_ai_agents.tools import ComputeQueryAlignment
from app.core.config import settings


def response_alignment_evaluation_node(state: dict) -> dict:
    """
    This node evaluates whether the LLM response actually addresses 
    and answers the user's original query.
    """
    # 1. Get query and response from state
    user_query = state.get("user_query", "")
    llm_response = state.get("llm_response", "")
    
    if not user_query or not llm_response:
        return {"alignment_results": {"score": 0, "error": "Missing query or response"}}

    # 2. Setup the LLM with Structured Output
    model = init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        api_key=settings.GEMINI_KEY,
    )
    structured_llm = model.with_structured_output(QueryAlignmentOutput)

    # 3. Format and invoke the prompt
    formatted_prompt = QUERY_ALIGNMENT_SYSTEM_PROMPT.format(
        user_query=user_query,
        llm_response=llm_response
    )

    alignment_analysis = structured_llm.invoke(formatted_prompt)

    # 4. Compute numerical score from verdict
    score = ComputeQueryAlignment.compute_alignment_score(alignment_analysis.alignment_verdict)

    # 5. Return only the updated keys for LangGraph
    return {"alignment_results": {"alignment_score": score, "alignment_analysis": alignment_analysis}}