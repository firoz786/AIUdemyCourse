"""
Day 19.04 - LangChain Tools (Integration) - chat model configuration.

Same local Ollama chat model setup as earlier days, used by the chain in
main.py.
"""

# ChatOllama is LangChain's wrapper around a locally running Ollama model.
from langchain_ollama import ChatOllama

# Create the chat model instance, pointing at the local "qwen3:1.7b" model.
model = ChatOllama(
    model="qwen3:1.7b"
)
