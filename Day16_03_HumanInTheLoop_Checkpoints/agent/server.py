"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This is the MCP "tool server" used by the demo: it exposes a few trivial
tools (get the current time, roll a dice, generate a password) over the
Model Context Protocol using `fastmcp`. The LangGraph agent in this project
connects to this server as a subprocess and calls these tools after a human
approves each call.
"""

from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; its name is shown to clients that connect.
mcp = FastMCP("Time Server")


# The @mcp.tool() decorator registers this function as a callable tool that
# MCP clients (our agent) can discover and invoke by name.
@mcp.tool()
def current_time():
    """Return the current date and time."""

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


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

    # Build the pool of allowed characters: letters, digits, and punctuation.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # secrets.choice is used (not random) because it's cryptographically
    # secure, which matters for generating passwords.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Running this file directly starts the MCP server and listens for
    # tool calls from a connected client (see agent/mcp_client.py).
    print("Starting MCP server..")
    mcp.run()
