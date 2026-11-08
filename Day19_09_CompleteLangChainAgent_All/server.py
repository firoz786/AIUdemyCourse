"""
Day 19.09 - MCP server exposing simple utility tools.

This script defines an MCP (Model Context Protocol) server with three
tools: get the current time, roll a dice, and generate a secure random
password. It is launched as a subprocess by mcp_tools.py (via stdio
transport) so that the LangChain agent in main.py / final_agent.py can
discover and call these tools.
"""

import random
import secrets
import string
from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; "Time Server" is just its display name.
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

    # Build the pool of characters a password can be made from.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # Pick `length` random characters using a cryptographically secure
    # generator (not the regular `random` module) since this is a password.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server; it will listen for tool calls over stdio.
    print("Starting MCP server..")
    mcp.run()
