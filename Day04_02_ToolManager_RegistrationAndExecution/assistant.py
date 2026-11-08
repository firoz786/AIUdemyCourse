"""
Day04_02_ToolManager_RegistrationAndExecution: upgrades Day04_01's loose tool
functions into a reusable `ToolManager` (see tool_manager.py) that maps text
commands like "dice" or "time" to a tool function, and runs them locally
without calling the LLM at all. This script also lets the user pick an
assistant "persona" (Teacher, Traveller, Comedian, etc.) via a system prompt,
then runs a chat loop where each user message is first checked against the
registered tools before falling back to asking the LLM. It demonstrates the
core pattern of registering tools and deciding, per message, whether to run
a tool or call the model.
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from tool_manager import ToolManager

# Each role maps a menu number to a (display name, behavior description)
# pair used to build the assistant's system prompt.
ROLES = {
    "1": ("Teacher", "Explain ideas clearly, step by step, with helpful examples."),
    "2": ("Traveller", "Answer like an experienced traveller, sharing practical travel tips."),
    "3": ("Comedian", "Respond with light, friendly humor while still answering the question."),
    "4": ("Politician", "Respond persuasively and diplomatically, considering different viewpoints."),
    "5": ("AI Expert", "Give knowledgeable, practical answers about artificial intelligence and related topics."),
}


def choose_role() -> tuple[str, str]:
    """Prompt for and return the selected assistant role and behavior."""
    print("Choose the assistant's behavior:")
    # Show the menu of available personas.
    for number, (role_name, _) in ROLES.items():
        print(f"{number}. {role_name}")

    # Keep asking until the user picks a valid option (1-5).
    while True:
        try:
            role_choice = input("Enter a number (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
            sys.exit(0)
        if role_choice in ROLES:
            return ROLES[role_choice]
        print("Please choose a number from 1 to 5.")


def create_messages(role_name: str, role_behavior: str) -> list[dict[str, str]]:
    """Create a conversation with the selected role as its system instruction."""
    # Build the system prompt that gives the model its persona for the
    # whole conversation.
    system_prompt = (
        f"You are an AI assistant acting as a {role_name}. {role_behavior} "
        "Give concise answers. If you don't know the answer, say you don't know."
    )
    return [{"role": "system", "content": system_prompt}]


def run_chat_loop(client: OpenAI, model: str, messages: list[dict[str, str]]) -> None:
    """Handle user input, local tools, and model responses."""
    # The tool manager knows how to match text commands (e.g. "dice") to
    # local Python functions, without needing the LLM.
    tool_manager = ToolManager()

    while True:
        # Ask the user for the next message. Handle Ctrl+C / Ctrl+D
        # gracefully so the program exits cleanly instead of crashing.
        try:
            input_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting the AI Assistant. Goodbye!")
            return

        # Let the user end the conversation with "exit" or "quit".
        normalized_input = input_text.casefold()
        if normalized_input in {"exit", "quit"}:
            print("Exiting the AI Assistant. Goodbye!")
            return
        if not input_text:
            continue

        # First, check if the input matches a registered local tool (e.g.
        # "dice", "time", "password"). If so, run it locally and skip the
        # LLM call entirely.
        tool_result = tool_manager.execute(input_text)
        if tool_result is not None:
            print(tool_result)
            continue

        # Otherwise, treat it as a normal chat message and ask the model.
        messages.append({"role": "user", "content": input_text})
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            answer = response.choices[0].message.content
            if not answer:
                answer = "(The model returned an empty response.)"
            print(f"AI: {answer}")
            # Save the reply so it becomes part of the context for the next turn.
            messages.append({"role": "assistant", "content": answer})
        except Exception as error:
            # If the API call failed, undo the user message we just added so
            # the conversation history doesn't contain an unanswered question.
            messages.pop()
            print(f"Error contacting the AI service: {error}")


def main() -> None:
    """Load configuration and start the interactive assistant."""
    # Load BASE_URL/API_KEY/MODEL from the .env file.
    load_dotenv()
    print(40 * "*")
    print(14 * " " + "AI Assistant")
    print(40 * "*")

    # Ask the user which persona the assistant should use.
    role_name, role_behavior = choose_role()
    model = os.getenv("MODEL")
    if not model:
        raise ValueError("MODEL is missing. Add MODEL to your .env file.")

    # Create the AI client used to talk to the LLM server.
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )
    # Seed the conversation with the chosen persona's system prompt.
    messages = create_messages(role_name, role_behavior)
    print(f"Assistant behavior: {role_name}\n")
    run_chat_loop(client, model, messages)


if __name__ == "__main__":
    main()
