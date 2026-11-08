"""
Day09_02_ReActAgent_FullLoop - agent/planner.py

This is the "Reason" part of the ReAct loop: it asks the LLM to look at
the user's request plus everything the agent has already done
(actions/observations from the state), and decide the single next action
to take -- or return "FINISH" once the request is fully satisfied.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (e.g. BASE_URL, API_KEY, MODEL) from .env.
load_dotenv()

# Create the AI client used to talk to the LLM provider.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):
    # Turn the list of MCP tool objects into one readable text block the
    # LLM can read, listing each tool's name and description.
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
    # Build the tool list text to embed in the prompt below.
    tool_descriptions = build_tool_descriptions(tools)

    # The prompt gives the LLM full context: the original request, what
    # has already been done, what was observed, and the available tools --
    # then asks it to pick exactly one next action (or FINISH).
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

    # The LLM's reply is expected to be just the tool name or "FINISH".
    return response.choices[0].message.content.strip()


