"""
Day 19.02 - Prompt Templates (Parameterized Text) - chat model config.

Same local Ollama chat model setup as Day 19.01, reused here so main.py
can focus on demonstrating prompt templates rather than model setup.
"""

# ChatOllama is LangChain's wrapper around a locally running Ollama model.
from langchain_ollama import ChatOllama

# Create the chat model instance, pointing at the local "qwen3:1.7b" model.
model = ChatOllama(
    model="qwen3:1.7b"
)
