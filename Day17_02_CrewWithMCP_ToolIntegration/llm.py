"""
Day 17.02 - CrewAI with MCP Tool Integration.

Defines the shared `LLM` instance used by every agent in this crew.
"""

from crewai import LLM

# A local Ollama-hosted model used by every agent in this demo.
llm = LLM(
    model="ollama/qwen3:1.7b"
)

