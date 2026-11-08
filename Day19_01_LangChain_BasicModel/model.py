"""
Day 19.01 - LangChain Basic Model - chat model configuration.

Creates the LangChain chat model instance (backed by a local Ollama
model) that main.py imports and invokes. Keeping the model definition in
its own module lets other scripts/tests reuse the same configured model
without repeating setup code.
"""

# ChatOllama is LangChain's wrapper around a locally running Ollama model.
from langchain_ollama import ChatOllama

# Create the chat model instance, pointing at the local "qwen3:1.7b" model.
model = ChatOllama(
    model="qwen3:1.7b"
)
