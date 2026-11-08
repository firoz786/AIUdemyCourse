"""
Day16_01 - LangGraph Basic Graph: MCP client helpers.

This module wraps the fastmcp Client so the rest of the lesson code can
connect to, query, and disconnect from our local MCP tool server
(agent/server.py) without worrying about the async context-manager
details. "Tools" discovered here are what the LangGraph planner node
chooses between.
"""

from pathlib import Path

from fastmcp import Client


async def connect():
    """
    Connect to the MCP Server.
    """

    # Wrap the relative script path in Path(...) so fastmcp receives a
    # proper path object instead of a bare string (avoids deprecation
    # warnings from APIs that expect os.PathLike inputs).
    client = Client(Path("agent/server.py"))

    # Manually enter the client's async context manager so we can keep the
    # connection open across multiple calls (instead of a single `async with`).
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):
    """
    Close the MCP connection.
    """

    # Manually exit the async context manager to cleanly shut the connection down.
    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):
    """
    Retrieve all tools from the server.
    """

    # Ask the MCP server what tools it exposes.
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

    # Default to no arguments if the caller didn't provide any.
    if arguments is None:
        arguments = {}

    # Ask the MCP server to run the named tool with the given arguments.
    result = await client.call_tool(
        tool_name,
        arguments
    )

    return result

