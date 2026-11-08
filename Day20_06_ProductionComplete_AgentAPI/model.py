"""
Day 20.06 - Production Complete Agent API.

Creates the shared LangChain chat model instance (a local Ollama model)
used everywhere in this project. Centralizing it here means every module
that needs an LLM imports the same configured `model` object instead of
each re-reading environment variables and re-constructing a client.
"""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load variables from a local .env file (e.g. MODEL_NAME, OLLAMA_BASE_URL)
# into the process environment, if such a file exists.
load_dotenv()

# Which Ollama model to use; falls back to a small default model if the
# environment variable isn't set.
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:1.7b"
)

# Where the local Ollama server is running.
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# The actual chat model object, shared/imported by agent.py, rag_tool.py,
# retriever.py (embeddings use a different model), etc.
model = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)
