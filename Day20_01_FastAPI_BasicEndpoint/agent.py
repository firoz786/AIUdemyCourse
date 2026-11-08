"""
Day 20.01 - Shared LangChain agent instance (no tools yet).

This module builds the LangChain agent used by main.py. At this stage of
the course the agent has no tools (`tools=[]`) - it is a plain
conversational LLM wrapped in the `create_agent` API, just enough to
expose through a FastAPI endpoint in main.py.
"""

from langchain.agents import create_agent

from model import model

# Create the agent object imported by main.py. No tools yet - this file
# focuses on wiring the agent into a FastAPI app, not on tool-calling.
agent = create_agent(
    model=model,
    tools=[]
)
