"""
Day 20.06 - Production Complete Agent API.

This is the MCP (Model Context Protocol) tool server referenced by
mcp_tools.py. It is launched as a separate subprocess and exposes three
simple tools (current time, dice roll, password generator) that the main
agent can call over stdio, demonstrating how tools can live outside the
main application process.
"""

import random
import secrets
import string
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


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""

    return random.randint(1, 6)


@mcp.tool()
def generate_password(length: int = 12):
    """
    Generate a secure password.
    """

    # Build the pool of characters a password can be made from: letters,
    # digits, and punctuation symbols.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # `secrets.choice` is used (instead of `random.choice`) because it is
    # cryptographically secure, which matters for generating passwords.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server and listen for tool calls over stdio.
    print("Starting MCP server..")
    mcp.run()
