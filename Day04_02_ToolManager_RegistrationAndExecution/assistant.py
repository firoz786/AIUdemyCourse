import os

from dotenv import load_dotenv
from openai import OpenAI

from tool_manager import ToolManager

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
    for number, (role_name, _) in ROLES.items():
        print(f"{number}. {role_name}")

    while True:
        role_choice = input("Enter a number (1-5): ").strip()
        if role_choice in ROLES:
            return ROLES[role_choice]
        print("Please choose a number from 1 to 5.")


def create_messages(role_name: str, role_behavior: str) -> list[dict[str, str]]:
    """Create a conversation with the selected role as its system instruction."""
    system_prompt = (
        f"You are an AI assistant acting as a {role_name}. {role_behavior} "
        "Give concise answers. If you don't know the answer, say you don't know."
    )
    return [{"role": "system", "content": system_prompt}]


def run_chat_loop(client: OpenAI, model: str, messages: list[dict[str, str]]) -> None:
    """Handle user input, local tools, and model responses."""
    tool_manager = ToolManager()

    while True:
        try:
            input_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting the AI Assistant. Goodbye!")
            return

        normalized_input = input_text.casefold()
        if normalized_input in {"exit", "quit"}:
            print("Exiting the AI Assistant. Goodbye!")
            return
        if not input_text:
            continue

        tool_result = tool_manager.execute(input_text)
        if tool_result is not None:
            print(tool_result)
            continue

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
            messages.append({"role": "assistant", "content": answer})
        except Exception as error:
            messages.pop()
            print(f"Error contacting the AI service: {error}")


def main() -> None:
    """Load configuration and start the interactive assistant."""
    load_dotenv()
    print(40 * "*")
    print(14 * " " + "AI Assistant")
    print(40 * "*")

    role_name, role_behavior = choose_role()
    model = os.getenv("MODEL")
    if not model:
        raise ValueError("MODEL is missing. Add MODEL to your .env file.")

    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )
    messages = create_messages(role_name, role_behavior)
    print(f"Assistant behavior: {role_name}\n")
    run_chat_loop(client, model, messages)


if __name__ == "__main__":
    main()
