"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This module implements the "brain" behind the planner node in graph.py.
Given the current agent state (what the user asked, what's been done so
far) and the list of available MCP tools, it asks an LLM to pick exactly
one next action (a tool name) or "FINISH". That choice is what the
`route_after_planner` conditional edge in graph.py uses to decide whether
the graph should run a tool next or jump to producing the final answer.
"""

import os

from openai import OpenAI
from dotenv import load_dotenv

# Load API keys / base URL / model name from a local .env file.
load_dotenv()

# Single shared OpenAI-compatible client used for every planner call.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):
    # Turn the list of MCP tool objects into one readable text block the
    # LLM can read inside its prompt, listing each tool's name/description.
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
    # Build the tool list text once so it can be embedded in the prompt.
    tool_descriptions = build_tool_descriptions(tools)

    # The prompt gives the LLM the user's goal, what's already been done,
    # and the rules for choosing exactly one next action (or FINISH).
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

    # Call the LLM to get its decision for the next action.
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

    # Strip whitespace so the returned string cleanly matches a tool name
    # or the literal "FINISH" used by the conditional routing logic.
    return response.choices[0].message.content.strip()

