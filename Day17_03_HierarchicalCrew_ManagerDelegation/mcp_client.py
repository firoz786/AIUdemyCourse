"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Thin async wrapper around the `fastmcp` client, used by the CrewAI tool in
mcp_tools.py to talk to the local MCP server (server.py). Provides connect,
disconnect, tool discovery, and tool execution helpers.
"""

from pathlib import Path

from fastmcp import Client


async def connect():
    """
    Connect to the MCP Server.
    """

    # Passing a Path (instead of a bare string) avoids a fastmcp deprecation
    # warning and is the recommended way to point the client at a script.
    client = Client(Path("server.py"))

    # Manually enter the client's async context manager so the connection
    # stays open across multiple calls instead of a single `with` block.
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):
    """
    Close the MCP connection.
    """

    # Manually exit the async context manager to cleanly close the connection.
    await client.__aexit__(None, None, None)


async def discover_tools(client):
    """
    Retrieve all tools from the server.
    """

    tools = await client.list_tools()

    return tools


async def execute_tool(client, tool_name, arguments=None):
    """
    Execute a tool.
    """

    # Default to an empty argument dict when the caller doesn't supply one.
    if arguments is None:
        arguments = {}

    result = await client.call_tool(tool_name, arguments)

    return result

