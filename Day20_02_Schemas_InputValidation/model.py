"""
Day 20.02 - Shared LLM instance, now configurable via environment variable.

This module loads settings from a local .env file (via python-dotenv)
and reads the model name from the MODEL_NAME environment variable,
falling back to "qwen3:1.7b" if it isn't set. This makes it easy to swap
models without editing code.
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

# Create the chat model using the configured model name.
model = ChatOllama(
    model=MODEL_NAME
)
