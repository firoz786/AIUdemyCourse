"""
Day 20.02 - Shared LangChain agent instance (no tools yet).

Same role as Day20_01's agent.py: builds the tool-less agent used by
main.py. This version's model.py now reads its model name from an
environment variable instead of hard-coding it.
"""

from langchain.agents import create_agent

from model import model

# Create the agent object imported by main.py. Still no tools - this
# folder's focus is input validation via Pydantic schemas (schemas.py).
agent = create_agent(
    model=model,
    tools=[]
)
