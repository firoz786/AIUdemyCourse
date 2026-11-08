"""
Day10_01_TaskPlanning_StructuredTasks - planner.py

This is the "Reason" step for the structured task-planning agent. Given
the current state (which includes the full task list and what's pending,
completed, observed, and resulted so far), it asks the LLM to pick exactly
one pending task and the best tool to complete it -- or reply FINISH once
no tasks remain.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

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

    # The prompt gives the LLM the full picture: the request, all tasks,
    # which ones are still pending, what's been done/observed/resulted so
    # far, and the available tools -- then asks for exactly one decision.
    prompt = f"""
You are an AI planner.

Your job is to select the next unfinished task
and the best tool to complete it.

User Request:

{state["user_request"]}

Tasks:

{state["tasks"]}

Pending Tasks:

{[
    item["task"]
    for item in state["tasks"]
    if item["status"] == "pending"
]}

Completed Actions:

{state["actions"]}

Observations:

{state["observations"]}

Intermediate Results:

{state["results"]}

Available Tools:

{tool_descriptions}

Rules:

1. Select only ONE pending task.

2. The TASK must be copied EXACTLY from the
   pending task list.

3. Do not change the task wording.

4. Do not select a completed task.

5. Select the best available tool for that task.

6. Use previous observations and results.

7. If an action failed, reconsider the task.

8. If there are no pending tasks,
   return ONLY the word:

FINISH

9. If tasks are still pending, return exactly
   two lines in this format:

TASK: <exact pending task>
TOOL: <tool_name>

10. Do not explain anything.

Next Decision:
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

    # The LLM's reply is expected to be either "FINISH" or the two-line
    # "TASK: ... / TOOL: ..." format parsed by loop.parse_decision().
    return response.choices[0].message.content.strip()
