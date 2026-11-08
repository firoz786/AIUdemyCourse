"""
Day 11.4 - Memory Advanced & Multi-Turn.

This module wraps the low-level FastMCP client calls used to talk to our
local MCP tool server (server.py): connecting, disconnecting, listing the
tools it exposes, and invoking a tool by name with arguments.
"""

from pathlib import Path

from fastmcp import Client


async def connect():

    """
    Connect to the MCP Server.
    """

    # Passing a Path (instead of a bare string) avoids a FastMCP
    # deprecation warning about string server paths.
    client = Client(Path("server.py"))

    # Manually enter the async context so the connection stays open
    # across multiple calls instead of closing right away.
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):

    """
    Close the MCP connection.
    """

    # Manually exit the async context to cleanly close the connection.
    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):

    """
    Retrieve all tools from the server.
    """

    # Ask the MCP server what tools it has registered.
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

    # Default to an empty argument dict when the caller doesn't pass any.
    if arguments is None:

        arguments = {}

    # Ask the MCP server to run the named tool with these arguments.
    result = await client.call_tool(

        tool_name,

        arguments

    )

    return result
