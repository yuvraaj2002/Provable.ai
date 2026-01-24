# Step 2 : Building the graph
from langgraph.graph import StateGraph, START, END
from app.provable_ai_agents.states import GeneratorEvaluationState
from app.provable_ai_agents.nodes import claim_extractor_node, groundness_evaluation_node, context_utilization_evaluation_node, response_alignment_evaluation_node, aggregator_node

workflow = StateGraph(GeneratorEvaluationState)

# Adding Nodes
workflow.add_node("extract_claims", claim_extractor_node)
workflow.add_node("groundness_check", groundness_evaluation_node)
workflow.add_node("utilization_check", context_utilization_evaluation_node)
workflow.add_node("alignment_check", response_alignment_evaluation_node)
workflow.add_node("aggregator", aggregator_node)

# Define Edges
workflow.set_entry_point("extract_claims")

# Fan-out: One node leads to three
workflow.add_edge("extract_claims", "groundness_check")
workflow.add_edge("extract_claims", "utilization_check")
workflow.add_edge("extract_claims", "alignment_check")

# Fan-in: All three must finish before aggregating
workflow.add_edge("groundness_check", "aggregator")
workflow.add_edge("utilization_check", "aggregator")
workflow.add_edge("alignment_check", "aggregator")

workflow.add_edge("aggregator", END)

# compiling the workflow
generator_evaluation_graph = workflow.compile()