"""
Day 20.03 - Shared LangChain agent instance (no tools yet).

Same role as earlier Day 20 agent.py files: builds the tool-less agent
used by main.py. This folder focuses on turning raw exceptions into
clean, user-facing HTTP errors (see main.py).
"""

from langchain.agents import create_agent

from model import model

# Create the agent object imported by main.py.
agent = create_agent(
    model=model,
    tools=[]
)
