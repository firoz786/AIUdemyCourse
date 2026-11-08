"""
Day 19.09 - Shared LLM instance for the capstone LangChain agent.

This module creates one `ChatOllama` model instance (pointing at a local
Ollama server running the qwen3:1.7b model) so that every other script in
this folder (agent, RAG chain, etc.) can import and reuse the same model
instead of each creating its own.
"""

from langchain_ollama import ChatOllama

# Create the chat model used everywhere in this folder. Ollama must be
# running locally with the "qwen3:1.7b" model already pulled.
model = ChatOllama(
    model="qwen3:1.7b"
)
