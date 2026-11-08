"""
Day 17.01 - CrewAI Role-Based Agents.

Defines the shared `LLM` instance that every agent in this crew uses to
"think" and generate responses. Centralizing it here means all agents stay
in sync if the model is ever changed.
"""

from crewai import LLM

# A local Ollama-hosted model used by every agent in this demo.
llm = LLM(
    model="ollama/qwen3:1.7b"
)

