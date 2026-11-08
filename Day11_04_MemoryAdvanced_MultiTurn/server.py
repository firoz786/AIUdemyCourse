"""
Day 11.4 - Memory Advanced & Multi-Turn.

This is the MCP tool server the agent connects to. It exposes three
simple tools over the Model Context Protocol (current time, dice roll,
password generator) that the planner can choose to call while working
through a user's request.
"""

from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; "Time Server" is its display name.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """Return the current date and time."""

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


import random


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""

    return random.randint(1, 6)


import secrets
import string


@mcp.tool()
def generate_password(length: int = 12):
    """
    Generate a secure password.
    """

    # Build the pool of characters a password can be made from.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # Use `secrets` (not `random`) since this generates security-sensitive data.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    print("Starting MCP server..")
    # Start listening for MCP client connections (blocks until stopped).
    mcp.run()

