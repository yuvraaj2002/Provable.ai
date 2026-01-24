from typing import TypedDict,List,Dict

class GeneratorEvaluationState(TypedDict):

    # Inputs
    user_query : str
    llm_response : str
    context_chunks : List[str]

    # Intermediate data
    atomic_claims: List[str]

    # Results
    groundness_results: Dict[str, any] # e.g., {"score": 1, "reason": "..."}
    utilization_results: Dict[str, any]
    alignment_results: Dict[str, any]
    
    # Final Report (from aggregator)
    final_report: Dict[str, any]