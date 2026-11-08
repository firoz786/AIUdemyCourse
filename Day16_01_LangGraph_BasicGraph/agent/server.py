"""
Day16_01 - LangGraph Basic Graph: MCP tool server.

This script defines the actual tools that the LangGraph planner node can
choose to call: getting the current time, rolling a dice, and generating
a random password. It uses FastMCP to expose plain Python functions as
MCP "tools" that agent/mcp_client.py connects to and agent/executor.py
invokes.
"""

import random
import secrets
import string
from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; its name shows up to connecting clients.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """Return the current date and time."""

    # Format as day-month-year hour:minute:second for easy reading.
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""

    # A simple random integer between 1 and 6, inclusive.
    return random.randint(1, 6)


@mcp.tool()
def generate_password(length: int = 12):
    """
    Generate a secure password.
    """

    # Combine letters, digits, and punctuation as the pool of characters.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # secrets.choice is cryptographically stronger than random.choice,
    # which matters for something security-sensitive like a password.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server so clients (agent/mcp_client.py) can connect.
    print("Starting MCP server..")
    mcp.run()
