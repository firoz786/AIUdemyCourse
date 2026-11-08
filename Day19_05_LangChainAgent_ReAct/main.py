"""
Day 19.05 - LangChain Agent (ReAct) - building a tool-using agent.

This is the capstone LangChain example: create_agent() builds a full
ReAct-style agent (Reason + Act) that can decide on its own which of the
three tools to call in order to answer the user's message, then returns
the final conversation. Unlike Day 19.04 (which calls a tool directly),
here the LLM itself chooses whether and which tool to invoke.
"""

# create_agent builds a ready-to-use tool-calling ReAct agent.
from langchain.agents import create_agent

from model import model
from tools import (
    current_time,
    roll_dice,
    generate_password
)

# Build the agent, giving it the chat model and the list of tools it is
# allowed to call.
agent = create_agent(
    model=model,
    tools=[
        current_time,
        roll_dice,
        generate_password
    ]
)

# Run the agent on a single user message; the agent decides internally
# whether a tool call is needed to answer it.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current time?"
            }
        ]
    }
)

# The agent returns the full message history; the last message is its
# final answer to the user.
print(result["messages"][-1].content)
