"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

The MCP "tool server": exposes current_time, roll_dice, and
generate_password tools via `fastmcp`. The CrewAI researcher agent reaches
this server (through mcp_client.py/mcp_tools.py) to fetch the real current
time while completing its task.
"""

from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; its name is shown to clients that connect.
mcp = FastMCP("Time Server")


# The @mcp.tool() decorator registers this function as a callable tool that
# MCP clients (our CrewAI agent) can discover and invoke by name.
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
    # tool calls from a connected client.
    print("Starting MCP server..")
    mcp.run()
