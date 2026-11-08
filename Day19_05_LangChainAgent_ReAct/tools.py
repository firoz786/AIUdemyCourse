"""
Day 19.05 - LangChain Agent (ReAct) - defining tools for the agent.

Defines the three tools made available to the ReAct agent in main.py,
using LangChain's @tool decorator so the agent's underlying LLM can
discover and call them automatically based on the user's request.
"""

# @tool turns a plain function into a LangChain tool the model can call.
from langchain_core.tools import tool


@tool
def current_time() -> str:
    """Return the current date and time."""
    # Imported locally so the module only pays the import cost when the
    # tool is actually used.
    from datetime import datetime

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@tool
def roll_dice() -> int:
    """Roll a six-sided dice."""
    import random

    return random.randint(1, 6)


@tool
def generate_password(length: int = 12) -> str:
    """Generate a random password."""

    # secrets is used instead of random for cryptographically strong
    # randomness, which is more appropriate for generating passwords.
    import secrets
    import string

    # Build the pool of characters a generated password can draw from.
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    # Pick `length` random characters from the pool and join them into
    # the final password string.
    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


