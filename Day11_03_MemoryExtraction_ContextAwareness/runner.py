"""
Day 11.3 - Memory Extraction & Context Awareness.

This is the entry-point script that ties everything together: it starts
the memory database, connects to the MCP tool server, discovers the
available tools, reads one request from the user, runs the full agent
loop (plan -> act -> observe, now with automatic memory extraction after
each answer), and prints the final answer before disconnecting.
"""

import asyncio
import sys

from mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from planner import planner
from executor import execute_action
from loop import run_agent_loop
from answer import format_answer
from memory import create_database


async def main():
    # Make sure the SQLite memory database/table exist before we use them.
    create_database()
    # Open a connection to the local MCP tool server.
    client = await connect()

    # Ask the server which tools it exposes (e.g. current_time, roll_dice).
    tools = await discover_tools(
        client
    )

    print("\nAvailable Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    # Ask the user what they'd like help with, handling Ctrl+C/EOF gracefully.
    try:
        user_request = input(
            "\nUser : "
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        await disconnect(client)
        sys.exit(0)

    # Run the full plan -> act -> observe loop for this single request.
    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        client
    )

    print("\nFinal Answer")
    print("------------")

    print(
        state["final_answer"]
    )

    # Cleanly close the MCP connection before the script exits.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())

