"""
Day02_02_ConversationMemory_MessageHistory: extends Day02_01 by making the
conversation's memory visible. After every reply, the script prints the
entire `messages` history (every past user and assistant turn) so learners
can literally see what context is being sent to the model on each call.
This makes the abstract idea of "conversation memory" concrete.
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
# conversation's "memory" that gets sent to the model on every turn.
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

    # Send the FULL conversation history so the model has context about
    # everything said before.
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

    # Print the whole conversation so far, so learners can see exactly what
    # "memory" the model has access to.
    print("\n========== Conversation History ==========")

    for message in messages:
        print(f"{message['role'].title()} : {message['content']}")

    print("==========================================")
