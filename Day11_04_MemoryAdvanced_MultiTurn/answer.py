"""
Day 11.4 - Memory Advanced & Multi-Turn.

This module is the final step of the agent loop: it turns everything the
agent has gathered (the user's request, any relevant long-term memories,
the task plan, the tool actions taken, and their results) into a single,
natural-language reply for the user. It hides all internal "agent
plumbing" (planner, tools, MCP, internal reasoning) so the answer reads
like a normal conversational response, which keeps multi-turn
conversations feeling natural.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load variables (BASE_URL, API_KEY, MODEL) from the .env file.
load_dotenv()

# Shared OpenAI-compatible client used to generate the final answer.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    """Build a prompt from the agent's state and ask the LLM to phrase
    a clean, user-facing answer from it."""

    prompt = f"""
The user asked:

{state["user_request"]}

Relevant previous memories:
{state["memories"]}

Tasks:
{state["tasks"]}

Actions:
{state["actions"]}

Observations:
{state["observations"]}

Intermediate Results:
{state["results"]}

Give the user a natural and concise answer.
Use relevant previous memories
when they help answer the user's question.


Do not mention:
- planner
- agent loop
- MCP
- internal state
- tools
- internal reasoning
"""

    # Ask the LLM to write the final answer based on the prompt above.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Return just the text of the reply, with extra whitespace trimmed.
    return response.choices[0].message.content.strip()

