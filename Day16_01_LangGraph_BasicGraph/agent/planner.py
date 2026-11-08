"""
Day16_01 - LangGraph Basic Graph: planner node logic.

This module contains the "brain" that the planner graph node (see
graph.py) calls on each run: it builds a prompt describing the user's
request, the tools available, and what's happened so far, then asks an
LLM to pick exactly one next action (a tool name) or "FINISH". This is
the same planning concept used throughout the course, just wired into a
LangGraph node instead of a plain Python loop.
"""

import os

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (BASE_URL, API_KEY, MODEL) from a .env file.
load_dotenv()

# A single shared OpenAI-compatible client used for every planner call.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):
    # Turn the list of MCP tool objects into a readable text block the
    # LLM can use to understand what each tool does.
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
    # Build the tool descriptions once per call so the prompt stays in sync
    # with whatever tools were discovered from the MCP server.
    tool_descriptions = build_tool_descriptions(tools)

    # The prompt instructs the LLM to return ONLY a tool name or "FINISH",
    # using the state's history so it doesn't repeat completed actions.
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

    # Call the LLM to get the planner's decision.
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

    # Strip whitespace so comparisons like `action == "FINISH"` work reliably.
    return response.choices[0].message.content.strip()

