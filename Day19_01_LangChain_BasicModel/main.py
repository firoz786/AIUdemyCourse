"""
Day 19.01 - LangChain Basic Model - invoking a chat model directly.

This is the simplest possible LangChain example: it imports a pre-built
chat model and calls .invoke() with a plain text prompt, then prints the
model's reply. It demonstrates the most basic building block of
LangChain - talking to an LLM - before later days add prompt templates,
chains, tools, and agents on top of it.
"""

# Import the already-configured chat model instance from model.py.
from model import model

# Send a single text prompt to the model and get back a response object.
response = model.invoke(
    "Explain what an AI agent is in two sentences."
)

# The actual generated text lives in the response's .content attribute.
print(response.content)
