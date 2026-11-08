"""
Day08_01_MCP_ServerAndClient: the MCP (Model Context Protocol) server side.
It exposes three simple tools (current time, dice roll, password generator)
using the `fastmcp` library's `@mcp.tool()` decorator. Any MCP-compatible
client (like mcp_client.py) can connect to this server, discover these
tools, and call them remotely - this is the "server" half of the client/
server tool-calling pattern.
"""

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

    # Build the pool of characters a password can be made from: letters,
    # digits, and punctuation symbols.
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    # Pick `length` random characters using `secrets` (a cryptographically
    # secure random generator, safer than `random` for passwords).
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    # Start the MCP server so it can accept client connections (this call
    # blocks and runs until the server process is stopped).
    print("Starting MCP server..")
    mcp.run()
