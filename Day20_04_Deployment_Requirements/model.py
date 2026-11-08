"""
Day 20.04 - Shared LLM instance, with configurable model name and base URL.

Extends Day20_03's model.py by also reading OLLAMA_BASE_URL from the
environment, so the Ollama server location can be changed per deployment
environment (local, Docker, staging, etc.) without touching code.
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
