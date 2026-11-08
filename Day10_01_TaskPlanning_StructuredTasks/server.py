"""
Day10_01_TaskPlanning_StructuredTasks - server.py

The MCP server side of the structured task-planning demo: a tiny FastMCP
server exposing three tools (current_time, roll_dice, generate_password)
that the Day10 agent (runner.py) can assign to the sub-tasks it plans.
"""

from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance with a human-readable name.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """Return the current date and time."""
    # Format the current timestamp as day-month-year hour:minute:second.
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


import random


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""
    # Return a random integer between 1 and 6, inclusive.
    return random.randint(1, 6)


import secrets
import string


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

    # Use `secrets` (not `random`) because it is cryptographically secure
    # and appropriate for generating passwords.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server and keep it running to serve tool requests.
    print("Starting MCP server..")
    mcp.run()
