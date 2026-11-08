"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This module turns the agent's internal action/observation history into a
single, natural-language answer for the end user. It makes one final LLM
call that is told to summarize the results conversationally, without
exposing internal planning details, state, or tool names.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (BASE_URL, API_KEY, MODEL) from a .env file.
load_dotenv()

# A single shared OpenAI-compatible client for generating the final answer.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    """Summarize the agent's actions/observations into a user-facing answer."""

    # Give the LLM the original question plus everything the agent did,
    # and ask it to respond as if it were answering directly (no internals).
    prompt = f"""
The user asked:

{state["user_request"]}

Actions performed:

{state["actions"]}

Observations:

{state["observations"]}

Answer the user naturally.

Do not mention internal planning.
Do not mention state.
Do not mention tools.
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

