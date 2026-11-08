"""
Day13_02 - Registry Agent: Dynamic Tool Discovery
===================================================
This module is the "brain" of the agent: it calls an LLM to decide the
single next action (which tool to call and with what arguments) based
on the user's request, the actions already taken, and what was
observed so far. The tool descriptions are built dynamically from
whatever tools the registry discovered, which is what makes this
agent's tool use "dynamic" rather than hard-coded.
"""
import json
import os

from openai import OpenAI
from dotenv import load_dotenv

# Load API credentials/config (BASE_URL, API_KEY, MODEL) from a .env file.
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):
    """Turn the list of discovered MCP tools into one readable text block for the prompt."""
    descriptions = ""

    for tool in tools:
        # Include the tool's name, description, and input schema so
        # the LLM knows exactly how to call it.
        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}

Input Schema:
{tool.inputSchema}

----------------------------
"""

    return descriptions


def planner(state, tools):
    """Ask the LLM to choose the next action, given the current agent state."""
    tool_descriptions = build_tool_descriptions(tools)

    # The prompt gives the LLM the full context (request, history so
    # far, available tools) and strict rules to keep its reply as
    # parseable JSON describing exactly one action.
    prompt = f"""
You are an AI Planner.

Your job is to decide ONLY the
next action.

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

2. Never repeat an action that has
   already been completed.

3. Use the observations to decide
   what is still required.

4. If the user's request has been
   completely satisfied, return FINISH.

5. Return ONLY valid JSON.

6. Do not explain your answer.

Use exactly this format:

{{
    "tool": "tool_name",
    "arguments": {{
        "argument_name": "argument_value"
    }}
}}

For FINISH, return:

{{
    "tool": "FINISH",
    "arguments": {{}}
}}

Next Action:
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "You are an AI planner."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()

    # The planner's reply must be valid JSON describing one action;
    # parse it into a dict for the rest of the loop to use.
    return json.loads(result)

