"""
Day10_01_TaskPlanning_StructuredTasks - answer.py

This module is the final "answer formatting" step of the structured task
planning agent: once the agent loop has decomposed the user's request into
tasks, executed tools for each, and gathered observations/results, this
function asks the LLM to turn all of that internal bookkeeping into one
natural, concise reply -- without leaking any of the planning/tooling
details to the end user.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (e.g. BASE_URL, API_KEY, MODEL) from .env.
load_dotenv()

# Create the AI client used to generate the final natural-language answer.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    # Summarize the whole run (request, tasks, actions, observations,
    # results) into a prompt and ask the LLM for a clean final answer.
    prompt = f"""
The user asked:

{state["user_request"]}

Tasks:
{state["tasks"]}

Actions:
{state["actions"]}

Observations:
{state["observations"]}

Intermediate Results:
{state["results"]}

Give the user a natural and concise answer.

Do not mention:
- planner
- agent loop
- MCP
- internal state
- tools
- internal reasoning
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


