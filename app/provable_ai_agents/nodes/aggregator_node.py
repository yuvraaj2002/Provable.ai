from app.provable_ai_agents.states import GeneratorEvaluationState

def aggregator_node(state: GeneratorEvaluationState) -> GeneratorEvaluationState:
    """
    Aggregator node that simply collects inputs from all previous nodes
    without performing any additional processing.
    """
    # The state already contains all the results from previous nodes
    # Just pass it through as-is
    return state