"""
Day07_02_AgentLoop_PlanActObserve: ties together planning and tools into a
full agent loop. For every user message the script: (1) PLAN - asks
`choose_tool` which tool (if any) fits the request; (2) ACT - calls that
tool locally to get a real result; (3) OBSERVE - feeds the tool's result
back into a prompt and asks the LLM to turn it into a natural-sounding
answer for the user. This Plan -> Act -> Observe cycle is the foundation of
how autonomous AI agents decide and take action.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

from planner import choose_tool

from tools import (
    get_current_time,
    roll_dice,
    generate_password
)

# Load configuration (BASE_URL, API_KEY, MODEL) from the local .env file.
load_dotenv()
# Create the AI client used to talk to the LLM server.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Simple banner so the user knows the chatbot is ready.
print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# Main agent loop: for every message, Plan -> Act -> Observe.
while True:

    # Ask the user to type a message. Handle Ctrl+C / Ctrl+D gracefully so
    # the program exits cleanly instead of crashing with a traceback.
    try:
        user_input = input("\nYou : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        break

    # Let the user end the conversation by typing "quit".
    if user_input.lower() == "quit":
            print("\nAI  : Goodbye! Have a great day.")
            break

    # PLAN: ask the LLM-based planner which tool (if any) matches this request.
    tool = choose_tool(user_input)

    # ACT: run the chosen tool locally to get a real, concrete result.
    if tool == "get_current_time":

        result = get_current_time()

    elif tool == "roll_dice":

        result = roll_dice()

    elif tool == "generate_password":

        result = generate_password()

    else:

        # No matching tool - the model will answer from its own knowledge.
        result = None

    # OBSERVE: combine the user's question and the tool's result into a
    # prompt, and ask the model to phrase a natural final answer.
    prompt = f"""
    The user asked:
    {user_input}
    The tool returned:
    {result}
    Answer the user naturally.don't add anything from your side in the answer. if tool is none, then answer it from llm model.
    """

    response = client.chat.completions.create(

            model=os.getenv("MODEL"),

            messages=[
                {
                "role":"user",
                "content":prompt
            }
                ]
                )
    print("\nAI :", response.choices[0].message.content)

