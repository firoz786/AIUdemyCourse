"""
Day 15 - Production Engineering & Resilience: LLM Call Wrapper with Retry/Backoff.

This file demonstrates the core "resilience" pattern for agents that depend on
an external LLM API: network calls and model servers can fail transiently, so
instead of letting one failure crash the whole agent, `call_llm` retries the
request up to MAX_RETRIES times, waiting progressively longer between
attempts (a simple linear backoff). Every attempt and failure is logged so
operators can see what happened, and if all retries are exhausted it raises a
clear error instead of failing silently.
"""

import time

# OpenAI's official Python client also works against OpenAI-compatible local
# servers like Ollama, since we point it at a custom BASE_URL.
from openai import OpenAI

# Centralized configuration values pulled in from config.py (env-driven).
from config import (
    BASE_URL,
    API_KEY,
    MODEL,
    MAX_RETRIES,
    TIMEOUT
)

# Shared logger so every LLM attempt/success/failure is recorded consistently.
from logger import logger


# Create a single, reusable client configured from our settings. Reusing one
# client avoids re-creating connections on every call.
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=TIMEOUT
)


def call_llm(messages):
    # Try the request up to MAX_RETRIES times before giving up.
    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:
            # Log every attempt number so failures are traceable in logs.
            logger.info(
                f"LLM request attempt {attempt}"
            )

            # Send the chat messages to the configured model and get a response.
            response = (
                client
                .chat
                .completions
                .create(
                    model=MODEL,
                    messages=messages
                )
            )

            logger.info(
                "LLM request successful"
            )

            # Extract just the text content of the model's reply.
            return (
                response
                .choices[0]
                .message
                .content
            )

        except Exception as e:
            # Catch any failure (timeout, connection error, bad response, etc.)
            # so we can retry instead of crashing the whole program.
            logger.error(
                f"LLM request failed: {e}"
            )

            if attempt == MAX_RETRIES:
                # We've used up all retries - fail loudly with a clear message.
                logger.error(
                    "Maximum retry limit reached"
                )

                raise RuntimeError(
                    "LLM request failed after "
                    f"{MAX_RETRIES} attempts."
                )

            # Simple linear backoff: wait longer after each failed attempt
            # before retrying, to avoid hammering a struggling server.
            wait_time = attempt * 2

            logger.info(
                f"Retrying in {wait_time} seconds"
            )

            time.sleep(
                wait_time
            )
