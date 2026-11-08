"""
Day 20.05 - Shared LangChain agent instance (no tools yet).

Same role as earlier Day 20 agent.py files. This folder's focus is
resilience: retrying failed agent calls and rate-limiting incoming
requests (see main.py).
"""

from langchain.agents import create_agent

from model import model

# Create the agent object imported by main.py.
agent = create_agent(
    model=model,
    tools=[]
)
