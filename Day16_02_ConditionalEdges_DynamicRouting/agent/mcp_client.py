"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This module wraps the `fastmcp` Client so the rest of the agent (executor,
main.py) doesn't need to know the details of connecting to, calling tools
on, or disconnecting from the local MCP tool server (`agent/server.py`).
It is used by the graph's "planner" node (to discover tools) and "tool"
node (to execute whichever action was chosen by the conditional routing
logic in `graph.py`).
"""

from pathlib import Path

from fastmcp import Client


async def connect():

    """
    Connect to the MCP Server.
    """

    # Wrap the server script path in Path(...) instead of passing a bare
    # string - this is the recommended way to point fastmcp's Client at a
    # local script file and avoids relying on implicit string-to-path
    # handling.
    client = Client(Path("agent/server.py"))

    # fastmcp's Client is an async context manager; entering it manually
    # (instead of `async with`) lets us keep the connection open across
    # multiple calls from main.py until we explicitly disconnect.
    await client.__aenter__()

    print("Connected to MCP Server.")

    return client


async def disconnect(client):

    """
    Close the MCP connection.
    """

    # Manually exit the async context manager to cleanly close the
    # connection that `connect()` opened above.
    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):

    """
    Retrieve all tools from the server.
    """

    # Ask the MCP server to list every tool it exposes (name + description
    # + schema), used by the planner to know what actions are available.
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

    # Default to an empty argument dict so callers can omit arguments for
    # tools that don't need any (e.g. current_time, roll_dice).
    if arguments is None:

        arguments = {}

    # Ask the MCP server to run the named tool with the given arguments
    # and return whatever result it produces.
    result = await client.call_tool(

        tool_name,

        arguments

    )

    return result

