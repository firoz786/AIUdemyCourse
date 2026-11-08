"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Exposes a CrewAI-compatible `@tool` function that, when called by an agent,
connects to the MCP server, invokes its `current_time` tool, and returns
the result as plain text. This bridges CrewAI's synchronous tool-calling
interface with the async MCP client.
"""

import asyncio

from crewai.tools import tool

from mcp_client import (
    connect,
    execute_tool,
    disconnect
)


async def call_mcp_current_time():
    """Open an MCP connection, call current_time, then always disconnect."""

    client = await connect()

    try:
        result = await execute_tool(client, "current_time")

        return result.content[0].text
    finally:
        await disconnect(client)


@tool("MCP Current Time")
def mcp_current_time() -> str:
    """Get the current date and time from MCP."""

    # CrewAI tools are called synchronously, so we use asyncio.run() to
    # drive the async MCP connection/call from this sync function.
    return asyncio.run(call_mcp_current_time())

