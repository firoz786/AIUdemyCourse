"""
Day03_01_SystemPrompts_AgentPersona: shows how a "system" message shapes the
AI's personality and behavior before any conversation happens. By seeding
`messages` with a system role ("You are a friendly AI teacher...") instead of
starting with an empty list, the same chat loop from Day02 now consistently
answers in a chosen persona/style. This demonstrates how system prompts are
used to give an agent a defined role.
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

# Simple banner so the user knows the chatbot is ready.
print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# Seed the conversation with a "system" message - this is not shown to the
# user but tells the model how to behave for the whole conversation (its
# persona/role), e.g. a friendly teacher that explains things simply.
messages = [
    {
        "role": "system",
        "content": "You are a friendly AI teacher. Explain every concept in simple language with real-life examples."
    }
]

# Main chat loop: keep asking the user for input until they quit.
while True:

    # Ask the user to type a message. Handle Ctrl+C / Ctrl+D gracefully so
    # the program exits cleanly instead of crashing with a traceback.
    try:
        user_input = input("\nYou : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        break

    # Save the user's message into the running conversation history.
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Let the user end the conversation by typing "quit".
    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    # Send the full conversation (system prompt + history) so the model
    # keeps its persona and context across turns.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    # Pull out the text of the model's reply.
    ai_reply = response.choices[0].message.content

    print("\nAI :", ai_reply)

    # Save the AI's reply too, so it is part of the context for the next turn.
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
