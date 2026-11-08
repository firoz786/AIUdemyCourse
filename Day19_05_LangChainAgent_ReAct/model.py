"""
Day 19.05 - LangChain Agent (ReAct) - chat model configuration.

Same local Ollama chat model setup as earlier days; this model powers the
ReAct agent built in main.py.
"""

# ChatOllama is LangChain's wrapper around a locally running Ollama model.
from langchain_ollama import ChatOllama

# Create the chat model instance, pointing at the local "qwen3:1.7b" model.
model = ChatOllama(
    model="qwen3:1.7b"
)
