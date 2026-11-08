"""
Day 19.07 - RAG with LangChain (Retrieval).

This module defines plain LangChain tools (decorated with @tool) used by
the shared MCP agent demo (main.py). They mirror the tools exposed by the
separate MCP server in server.py.
"""

from langchain_core.tools import tool  # Decorator that turns a function into a LangChain-callable tool.


@tool
def current_time() -> str:
    """Return the current date and time."""
    from datetime import datetime  # Imported here to keep the import close to its single use.

    # Format and return the current timestamp as a string.
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@tool
def roll_dice() -> int:
    """Roll a six-sided dice."""
    import random  # Imported here, only needed by this tool.

    # Simulate a dice roll: a random integer from 1 to 6.
    return random.randint(1, 6)


@tool
def generate_password(length: int = 12) -> str:
    """Generate a random password."""

    import secrets  # Cryptographically secure randomness for password generation.
    import string  # Supplies the character sets used to build the password.

    # Pool of characters the generated password can draw from.
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    # Randomly select `length` characters and join them into the final password.
    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


