"""
Day 20.04 - Shared LangChain agent instance (no tools yet).

Same role as earlier Day 20 agent.py files. This folder's focus is
packaging/deployment concerns (requirements.txt, configurable Ollama
base URL) rather than the agent logic itself.
"""

from langchain.agents import create_agent

from model import model

# Create the agent object imported by main.py.
agent = create_agent(
    model=model,
    tools=[]
)
