"""
Day 19.03 - Chain Operator (Piping) - chat model configuration.

Same local Ollama chat model setup as earlier days; this is one of the
pieces piped together with `|` in main.py.
"""

# ChatOllama is LangChain's wrapper around a locally running Ollama model.
from langchain_ollama import ChatOllama

# Create the chat model instance, pointing at the local "qwen3:1.7b" model.
model = ChatOllama(
    model="qwen3:1.7b"
)
