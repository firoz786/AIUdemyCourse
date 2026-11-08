"""
Day01_01_ChatBasics_FirstLLMCall: the simplest possible example of calling a
Large Language Model (LLM). This script sends one hard-coded question to the
model and prints the single reply it gets back - there is no loop, no memory,
and no user input. It is meant to show the bare minimum code needed to talk
to an LLM through an OpenAI-compatible API before we add conversation loops,
system prompts, or tools in later lessons.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration (BASE_URL, API_KEY, MODEL) from the local .env file.
load_dotenv()

# Create a client that communicates with the LLM server (e.g. Ollama) using
# the OpenAI-compatible API format.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Send one question to the AI model as a single "user" message and wait for
# the model's reply (this call blocks until the full response is ready).
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is Artificial Intelligence?"
        }
    ]
)

# Extract and print just the text content of the model's first (and only)
# reply choice.
print(response.choices[0].message.content)
