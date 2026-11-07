import asyncio

from crewai.tools import tool

from mcp_client import (
    connect,
    execute_tool,
    disconnect
)


async def call_mcp_current_time():

    client = await connect()

    try:

        result = await execute_tool(
            client,
            "current_time"
        )

        return result.content[0].text

    finally:

        await disconnect(client)


@tool("MCP Current Time")
def mcp_current_time() -> str:
    """Get the current date and time from MCP."""

    return asyncio.run(
        call_mcp_current_time()
    )
