"""
Day08_02_MCPAgent_IntegratedLoop - mcp_client.py

Small helper module that wraps the lifecycle of talking to an MCP server:
connecting, listing tools, calling a tool, and disconnecting. Keeping this
logic in one place means every script in this folder (agent.py,
test_client.py) can reuse the same connection code instead of repeating it.
"""

from pathlib import Path

# fastmcp's Client expects a Path (not a bare string) for local server
# scripts; passing a string is deprecated and triggers a
# FastMCPDeprecationWarning, so we wrap the filename in Path(...).
from fastmcp import Client


async def connect():
    """
    Connect to the MCP Server.
    """
    # Point the client at our local server.py script using a Path object.
    client = Client(Path("server.py"))

    # Manually enter the async context manager so we can keep the
    # connection open across multiple function calls (instead of using
    # a single `async with` block).
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):
    """
    Close the MCP connection.
    """
    # Manually exit the async context manager to cleanly close the session.
    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):
    """
    Retrieve all tools from the server.
    """
    # Ask the server what tools it exposes (name, description, schema, etc.).
    tools = await client.list_tools()

    return tools


async def execute_tool(
    client,
    tool_name,
    arguments=None
):
    """
    Execute a tool.
    """
    # Default to an empty dict so callers don't need to pass arguments
    # when a tool takes none.
    if arguments is None:
        arguments = {}

    # Ask the MCP server to run the named tool with the given arguments.
    result = await client.call_tool(
        tool_name,
        arguments
    )

    return result

