"""
Day 19.09 - Local LangChain tools (non-MCP version).

This module defines the same three utility tools as server.py
(current_time, roll_dice, generate_password), but as plain LangChain
`@tool`-decorated Python functions instead of MCP tools. It is useful for
comparing "local tool" vs "MCP tool" integration styles, and is used by
test_tool.py.
"""

from langchain_core.tools import tool


@tool
def current_time() -> str:
    """Return the current date and time."""
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

    import secrets
    import string

    # Pool of characters the generated password can draw from.
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    # Use a cryptographically secure random choice for each character.
    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


