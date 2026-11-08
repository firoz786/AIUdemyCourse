"""
Day 19.08 - Memory with LangChain (Conversation).

This module creates the chat model used throughout the conversational
memory examples in this folder (memory_demo.py, memory_with_history.py) as
well as the shared MCP agent demo. It wires up a local Ollama model
("qwen3:1.7b") through LangChain's ChatOllama wrapper so other scripts can
simply `from model import model`.
"""

from langchain_ollama import ChatOllama  # Current, non-deprecated LangChain wrapper for local Ollama models.

# Create the chat model instance that chains and agents will reason with.
model = ChatOllama(
    model="qwen3:1.7b"
)
