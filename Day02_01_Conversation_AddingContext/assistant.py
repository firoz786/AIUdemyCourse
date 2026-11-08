"""
Day02_01_Conversation_AddingContext: builds on Day01's single-shot chatbot by
adding "context" - a running list of every message exchanged so far. Instead
of sending only the latest question, each request now sends the entire
`messages` list to the model, so the AI can refer back to earlier parts of
the conversation (e.g. "what did I just ask you?"). This is the first step
toward giving an LLM memory of a conversation.
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

# This list accumulates every user and assistant message so far - it is the
# "context" that gets sent to the model on every turn.
messages = []

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

    # Send the FULL conversation history (not just the latest message) so
    # the model has context about everything said before.
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
