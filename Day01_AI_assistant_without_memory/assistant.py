from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print(40 * "*")
print(14 * " " + "AI Assistant")
print(40 * "*")

while True:
    input_text = input("You: ")
    if input_text.lower() in ["exit", "quit"]:
        print("Exiting the AI Assistant. Goodbye!")
        break 
    response = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL")).chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "user", "content": input_text}],
    )
 
    print("AI: " + response.choices[0].message.content)