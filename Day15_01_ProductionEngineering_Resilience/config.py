"""
Day 15 - Production Engineering & Resilience: Configuration Management.

This file demonstrates the "configuration" pillar of building production-grade
AI agents: instead of hard-coding values like model names, URLs, or retry
counts directly in the code, we read them from environment variables (with
safe fallback defaults). This makes the agent system easy to reconfigure for
different environments (dev/test/prod) without touching any code, which is a
key resilience practice - config changes shouldn't require a redeploy.
"""

import os

# python-dotenv lets us load variables from a local .env file into the
# process environment, so secrets/config stay out of source control.
from dotenv import load_dotenv

# Load the .env file (if present) before we read any environment variables.
load_dotenv()


# Which LLM model to use. Falls back to a small local Ollama model if the
# MODEL environment variable isn't set.
MODEL = os.getenv(
    "MODEL",
    "qwen3:1.7b"
)


# Base URL of the OpenAI-compatible API endpoint (defaults to a local Ollama
# server) so the same code can point at different providers via .env.
BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:11434/v1"
)


# API key used to authenticate with the LLM endpoint. "ollama" is a
# placeholder value accepted by local Ollama servers that don't check keys.
API_KEY = os.getenv(
    "API_KEY",
    "ollama"
)


# Maximum number of coding/review revision cycles the manager agent will
# allow before giving up, to prevent infinite retry loops.
MAX_REVISIONS = int(
    os.getenv(
        "MAX_REVISIONS",
        "8"
    )
)


# Maximum number of times a failed LLM call will be retried before raising
# an error - a core resilience/backoff setting.
MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "3"
    )
)


# How many seconds to wait for an LLM response before timing out, so a slow
# or hung request doesn't block the agent forever.
TIMEOUT = int(
    os.getenv(
        "TIMEOUT",
        "60"
    )
)

