"""
Day07_01_Planning_ChooseTool: introduces the "Planning" step of an agent
loop. Instead of running tools or calling the model directly, `choose_tool`
asks the LLM itself to act as a planner: given the user's request and a
short list of available tools, the model decides WHICH tool (if any) should
be used, by name only. The actual tool is not executed here - this file only
demonstrates the decision-making step that would normally come before
"Act" and "Observe" in a Plan -> Act -> Observe agent loop.
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


