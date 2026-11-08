"""
Day13_01 - MCP Registry: Connecting to Multiple Servers
========================================================
This is one of the two independent MCP servers merged by the registry
demo in this folder. It exposes small utility tools (current time,
dice roll, password generator) over the Model Context Protocol so an
agent (or the registry in mcp_manager.py) can discover and call them
without needing to import this code directly.
"""
import random
import secrets
import string
from datetime import datetime

from fastmcp import FastMCP

# Create the MCP server instance; the name shows up when clients connect.
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """Return the current date and time."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice."""
    return random.randint(1, 6)


@mcp.tool()
def generate_password(length: int = 12):
    """
    Generate a secure password.
    """
    # Build an alphabet of letters, digits, and punctuation to draw from.
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Use `secrets` (not `random`) for password generation since it's
    # cryptographically secure and appropriate for generating secrets.
    return "".join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    print("Starting MCP server..")
    # Run the server; FastMCP handles the stdio/transport loop.
    mcp.run()
