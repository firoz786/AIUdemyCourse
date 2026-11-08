"""
Day 19.06 - MCP Integration with LangChain.

This module creates the chat model used throughout the examples in this
folder. It wires up a local Ollama model ("qwen3:1.7b") through LangChain's
ChatOllama wrapper so other scripts can simply `from model import model`.
"""

from langchain_ollama import ChatOllama  # Current, non-deprecated LangChain wrapper for local Ollama models.

# Create the chat model instance that agents and chains will reason with.
model = ChatOllama(
    model="qwen3:1.7b"
)
