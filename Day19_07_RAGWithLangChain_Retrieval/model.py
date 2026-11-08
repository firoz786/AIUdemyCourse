"""
Day 19.07 - RAG with LangChain (Retrieval).

This module creates the chat model used throughout the RAG example in this
folder (rag.py) as well as the shared MCP agent demo. It wires up a local
Ollama model ("qwen3:1.7b") through LangChain's ChatOllama wrapper so other
scripts can simply `from model import model`.
"""

from langchain_ollama import ChatOllama  # Current, non-deprecated LangChain wrapper for local Ollama models.

# Create the chat model instance that chains and agents will reason with.
model = ChatOllama(
    model="qwen3:1.7b"
)
