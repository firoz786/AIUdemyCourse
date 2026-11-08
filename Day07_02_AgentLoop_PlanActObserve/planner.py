"""
Day07_02_AgentLoop_PlanActObserve: implements the "Plan" step used by
assistant.py. `choose_tool` asks the LLM to read the user's request and the
list of available tools, then respond with just the matching tool's name
(or "none"). The agent loop then uses this decision to decide what to ACT on.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration (BASE_URL, API_KEY, MODEL) from the local .env file.
load_dotenv()

# Create the AI client used to talk to the LLM server.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def choose_tool(user_request):
    """Ask the LLM to pick which tool (if any) best matches the user's request."""

    # Describe the available tools and ask the model to reply with just the
    # matching tool's name (or "none" if no tool is needed).
    planner_prompt = f"""
You are an AI planner.

Available tools:

1. get_current_time
   Use when the user asks for the current date or time.

2. roll_dice
   Use when the user asks to roll a dice.

3. generate_password
   Use when the user wants a secure password.

If no tool is required, return:

none

Return ONLY the tool name.

User Request:

{user_request}
"""

    # Send the planning prompt to the model as a one-off request (no
    # conversation history is needed for this decision).
    response = client.chat.completions.create(

        model=os.getenv("MODEL"),

        messages=[
            {
                "role": "system",
                "content": "You are an AI planner."
            },
            {
                "role": "user",
                "content": planner_prompt
            }
        ]
    )

    # Return just the chosen tool name, with any surrounding whitespace removed.
    return response.choices[0].message.content.strip()


