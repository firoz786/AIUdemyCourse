"""
Day01_01_ChatBasics_FirstLLMCall: a minimal interactive chatbot built on top
of the single-call example in hello_ai.py. Instead of asking one fixed
question, this script keeps looping: it reads whatever the user types,
sends it to the LLM, prints the reply, and repeats until the user types
"quit". This demonstrates the basic read -> send -> print loop that every
chat-style AI assistant is built on, before memory or system prompts are
introduced in later days.
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

# Main chat loop: keep asking the user for input until they quit.
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

    # Send the user's message to the model as a single "user" turn (no
    # history is kept here - each question is sent in isolation).
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    # Print just the text of the model's reply.
    print("\nAI :", response.choices[0].message.content)

