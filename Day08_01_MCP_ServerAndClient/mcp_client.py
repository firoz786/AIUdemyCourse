"""
Day08_01_MCP_ServerAndClient: client-side helper functions for talking to an
MCP (Model Context Protocol) server over its own process. MCP is a standard
protocol that lets an AI client discover and call tools exposed by a
separate server process (see server.py), instead of defining tools directly
inside the client's code. This file wraps the raw fastmcp `Client` API with
simple async functions: connect, disconnect, list available tools, and call
a tool by name.
"""

from pathlib import Path

from fastmcp import Client


async def connect():

    """
    Connect to the MCP Server.
    """

    # Pass a Path (not a bare string) to Client() - this points fastmcp at
    # the server.py script to launch and avoids a deprecation warning for
    # string paths.
    client = Client(Path("server.py"))

    # Open the connection (equivalent to entering an `async with` block
    # manually, since we want to keep the connection open across calls).
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):

    """
    Close the MCP connection.
    """

    # Properly close the connection we opened manually in connect().
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

    if arguments is None:

        arguments = {}

    # Ask the MCP server to run the named tool with the given arguments.
    result = await client.call_tool(

        tool_name,

        arguments

    )

    return result

