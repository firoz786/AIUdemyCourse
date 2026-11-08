"""
Day 19.07 - RAG with LangChain (Retrieval).

This is the MCP server process used by the shared agent demo (main.py). It
exposes three simple tools (current_time, roll_dice, generate_password)
over the Model Context Protocol so an MCP client can discover and call
them from a LangChain agent running in a different process.
"""

from datetime import datetime  # Used by current_time() to read the system clock.

from fastmcp import FastMCP  # Framework that turns plain Python functions into MCP tools.

# Create the MCP server instance; "Time Server" is just its display name.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """Return the current date and time."""
    # Format the current timestamp as day-month-year hour:minute:second.
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


import random  # Used by roll_dice() to pick a random number.


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""
    # Return a random integer between 1 and 6 inclusive, like a real dice roll.
    return random.randint(1, 6)


import secrets  # Cryptographically secure random choices, safer than `random` for passwords.
import string  # Provides the character sets (letters, digits, punctuation) to build from.


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

    # Randomly pick `length` characters from the pool and join them into a string.
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server; it will block here and listen for client requests.
    print("Starting MCP server..")
    mcp.run()
