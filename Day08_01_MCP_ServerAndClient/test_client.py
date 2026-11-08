"""
Day08_01_MCP_ServerAndClient: an end-to-end demo that starts an MCP client,
connects to the Time Server (server.py), lists the tools it exposes, calls
the "roll_dice" tool remotely, and prints the result. This shows the full
MCP client/server flow: connect -> discover tools -> call a tool -> read
the result -> disconnect.
"""

import asyncio

from mcp_client import *


async def main():

    # Connect to the MCP server (this launches/attaches to server.py).
    client = await connect()

    # Ask the server what tools are available.
    tools = await discover_tools(
        client
    )

    print()

    print("Available Tools")

    print("----------------")

    # List each tool's name so we can see what the server exposes.
    for tool in tools:

        print(tool.name)

    print()

    # Call the "roll_dice" tool remotely via MCP (no local arguments needed).
    result = await execute_tool(

        client,

        "roll_dice"

    )

    # The MCP result wraps the tool's output in a content list; grab the
    # first item's text.
    print("Dice Result:", result.content[0].text)

    # Always close the connection when we're done with it.
    await disconnect(
        client
    )


# Run the async demo from top to bottom.
asyncio.run(main())
