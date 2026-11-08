"""
Day08_03_AdvancedMCP_ErrorHandling - mcp_client.py

Small helper module that wraps the lifecycle of talking to an MCP server:
connecting, listing tools, calling a tool, and disconnecting. Centralizing
this logic means agent.py and test_client.py in this folder can reuse the
same connection code. NOTE: this file already uses `Client(Path("server.py"))`
instead of a bare string, which avoids the FastMCPDeprecationWarning that
older fastmcp versions raise when a plain string path is passed to Client().
"""

from pathlib import Path

from fastmcp import Client


async def connect():
    """
    Connect to the MCP Server.
    """
    # Wrapping the filename in Path(...) (instead of a bare string) is the
    # modern, non-deprecated way to point fastmcp's Client at a local
    # server script.
    client = Client(Path("server.py"))

    # Manually enter the async context manager so the connection stays
    # open across multiple function calls.
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

