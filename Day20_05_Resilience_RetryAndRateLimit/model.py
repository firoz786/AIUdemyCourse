"""
Day 20.05 - Shared LLM instance, with configurable model name and base URL.

Same as Day20_04's model.py: reads MODEL_NAME and OLLAMA_BASE_URL from
the environment (via a .env file), so both can be changed per deployment
without touching code.
"""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load variables from a .env file (if present) into the environment.
load_dotenv()

# Read the model name from the environment, defaulting if not set.
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:1.7b"
)

# Read where the Ollama server lives, defaulting to localhost.
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# Create the chat model, pointed at the configured Ollama instance.
model = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)
