from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print(40 * "*")
print(14 * " " + "AI Assistant")
print(40 * "*")

roles = {
    "1": ("Teacher", "Explain ideas clearly, step by step, with helpful examples."),
    "2": ("Traveller", "Answer like an experienced traveller, sharing practical travel tips."),
    "3": ("Comedian", "Respond with light, friendly humor while still answering the question."),
    "4": ("Politician", "Respond persuasively and diplomatically, considering different viewpoints."),
    "5": ("AI Expert", "Give knowledgeable, practical answers about artificial intelligence and related topics."),
}

print("Choose the assistant's behavior:")
for number, (role_name, _) in roles.items():
    print(f"{number}. {role_name}")

while True:
    role_choice = input("Enter a number (1-5): ").strip()
    if role_choice in roles:
        break
    print("Please choose a number from 1 to 5.")

role_name, role_behavior = roles[role_choice]
print(f"Assistant behavior: {role_name}\n")

# Keep the same conversation list for the whole program. This lets the model
# use earlier messages when answering later questions.
messages = [
    {
        "role": "system",
        "content": f"You are an AI assistant acting as a {role_name}. {role_behavior} Give concise answers. If you don't know the answer, say you don't know.",
    }
]

# Create the client once instead of recreating it for every message.
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)
model = os.getenv("MODEL")

if not model:
    raise ValueError("MODEL is missing. Add MODEL to your .env file.")

while True:
    try:
        input_text = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting the AI Assistant. Goodbye!")
        break

    if input_text.lower() in {"exit", "quit"}:
        print("Exiting the AI Assistant. Goodbye!")
        break

    if not input_text:
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
        print("AI: " + answer)
        messages.append({"role": "assistant", "content": answer})
    except Exception as error:
        # Remove the unanswered user message so it won't be sent again later.
        messages.pop()
        print(f"Error contacting the AI service: {error}")
