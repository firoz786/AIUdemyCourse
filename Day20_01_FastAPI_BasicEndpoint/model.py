"""
Day 20.01 - Shared LLM instance for the basic FastAPI endpoint example.

This module creates the `ChatOllama` model instance used by agent.py. It
is the simplest version seen in Day 20: the model name is hard-coded
(later days read it from an environment variable instead).
"""

from langchain_ollama import ChatOllama

# Create the chat model; Ollama must be running locally with this model
# already pulled (e.g. `ollama pull qwen3:1.7b`).
model = ChatOllama(
    model="qwen3:1.7b"
)
