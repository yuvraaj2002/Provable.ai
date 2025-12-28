"""
LLM Service

Service layer for interacting with agents and LLM functionality.
Agents are imported from the agents module following Google ADK best practices.
"""

from app.agents import root_agent

__all__ = ["root_agent"]