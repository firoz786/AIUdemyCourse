"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This module is the "brain" of the agent loop: it asks an LLM (via the
OpenAI-compatible API) to decide, step by step, which single tool to run
next based on the user's request, what's already been done, and what was
observed so far. It returns either a tool name or the literal "FINISH".
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (BASE_URL, API_KEY, MODEL) from a .env file.
load_dotenv()

# A single shared OpenAI-compatible client, configured from the environment
# so this demo can work with OpenAI or any compatible local/remote endpoint.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):
    """Turn the MCP tool list into a readable block of text for the LLM prompt."""

    descriptions = ""

    for tool in tools:
        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}

----------------------------
"""

    return descriptions


def planner(state, tools):
    """Ask the LLM which single next action to take, given the current state."""

    tool_descriptions = build_tool_descriptions(tools)

    # The prompt gives the LLM everything it needs to make one decision:
    # the user's goal, what's already happened, and the tools it can pick from.
    prompt = f"""
You are an AI Planner.

Your job is to decide ONLY the next action.

User Request:
{state["user_request"]}

Completed Actions:
{state["actions"]}

Previous Observations:
{state["observations"]}

Available Tools:
{tool_descriptions}

Rules:

1. Choose only ONE next action.
2. Never repeat an action that has already been completed.
3. Use the observations to decide what is still required.
4. If the user's request has been completely satisfied, return FINISH.
5. Return ONLY the tool name or FINISH.
6. Do not explain your answer.

Next Action:
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Strip whitespace so the returned value is a clean tool name or "FINISH".
    return response.choices[0].message.content.strip()

