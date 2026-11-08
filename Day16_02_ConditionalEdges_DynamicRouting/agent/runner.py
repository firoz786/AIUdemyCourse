"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This module implements the "answer" node's logic in graph.py. Once the
conditional routing decides the agent is finished (either the planner
returned FINISH, or the max_steps safety limit was hit), this function
turns the full history of actions/observations into one natural-language
reply for the user.
"""

import os

from openai import OpenAI
from dotenv import load_dotenv

# Load API keys / base URL / model name from a local .env file.
load_dotenv()

# Single shared OpenAI-compatible client used to generate the final answer.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    # Build a prompt that gives the LLM everything it needs to summarize
    # the work done, without exposing internal planning/tool details.
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

    # Ask the LLM to turn the raw history into a natural-sounding answer.
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

