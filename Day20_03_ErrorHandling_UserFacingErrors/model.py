"""
Day 20.03 - Shared LLM instance, configurable via environment variable.

Same as Day20_02's model.py: loads a .env file and reads MODEL_NAME from
the environment, defaulting to "qwen3:1.7b" if not set.
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
