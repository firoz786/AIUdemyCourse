from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print(40 * "*")
print(14 * " " + "AI Assistant")
print(40 * "*")

# Keep the same conversation list for the whole program. This lets the model
# use earlier messages when answering later questions.
messages = []

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
