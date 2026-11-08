"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Defines two `LLM` instances: `llm` is used by the worker agents
(researcher/coder/reviewer), while `manager_llm` is used by CrewAI's
internal manager in the hierarchical process to decide which agent should
handle each task.
"""

from crewai import LLM

# The model used by the worker agents.
llm = LLM(
    model="ollama/qwen3:1.7b"
)

# The model used by the hierarchical crew's manager to delegate tasks.
manager_llm = LLM(
    model="ollama/qwen3:1.7b"
)


