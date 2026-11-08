"""
Day08_02_MCPAgent_IntegratedLoop - test_client.py

Quick manual smoke-test script for the MCP client helpers in this folder.
It connects to the MCP server, lists the tools it finds, calls the
`roll_dice` tool to prove execute_tool() works end-to-end, prints the
result, and disconnects. This is not a pytest/unittest suite -- it is a
simple script you run directly to sanity-check the connection.
"""

import asyncio

from mcp_client import *

async def main():
    # Step 1: Connect to the MCP server.
    client = await connect()

    # Step 2: Discover the tools the server exposes.
    tools = await discover_tools(
        client
    )

    print()

    print("Available Tools")

    print("----------------")

    # Print each discovered tool's name.
    for tool in tools:

        print(tool.name)

    print()

    # Step 3: Actually call a tool ("roll_dice") to prove execution works.
    result = await execute_tool(

        client,

        "roll_dice"

    )

    print("Dice Result:", result.content[0].text)

    # Step 4: Disconnect cleanly from the server.
    await disconnect(
        client
    )


asyncio.run(main())
