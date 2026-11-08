"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This is the MCP "tool server" used by this lesson. It exposes three simple
tools (current_time, roll_dice, generate_password) over MCP so the agent
built in graph.py/main.py can call them. The LangGraph planner node decides
WHICH of these tools to call next, and the conditional edges decide WHEN
to stop calling tools and move to the final answer - this file just
implements what each tool actually does.
"""

import random
import secrets
import string
from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance that will host our tools.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():

    """Return the current date and time."""

    # Format the current timestamp as a simple day-month-year/time string.
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


@mcp.tool()
def roll_dice():

    """Roll a six-sided dice."""

    # Random integer between 1 and 6 inclusive, like a physical die.
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

    # Use `secrets` (not `random`) because it's cryptographically secure,
    # which matters when generating something like a password.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server so main.py's client can connect and call tools.
    print("Starting MCP server..")
    mcp.run()
