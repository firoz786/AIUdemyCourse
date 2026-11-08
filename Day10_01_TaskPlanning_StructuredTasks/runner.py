"""
Day10_01_TaskPlanning_StructuredTasks - runner.py

This is the entry point that ties the structured task-planning agent
together: it connects to the MCP server, discovers tools, reads the
user's goal, runs the full task-decomposition + planner + executor loop
(run_agent_loop), and prints the final natural-language answer. Run this
file directly to see Day10's structured task planning agent in action.
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


async def main():
    # Step 1: Connect to the MCP Server.
    client = await connect()

    # Step 2: Discover all available tools exposed by the server.
    tools = await discover_tools(
        client
    )

    print("\nAvailable Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    # Step 3: Ask the user for their goal. Wrapped in try/except so that
    # Ctrl+C (KeyboardInterrupt) or an unexpected end-of-input (EOFError)
    # exits the program gracefully instead of printing a scary traceback.
    try:
        user_request = input(
            "\nUser : "
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # Step 4: Run the structured task-planning loop: decompose the goal
    # into tasks, then plan/execute/observe until all tasks are complete.
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

    # Step 5: Always disconnect cleanly from the MCP server.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())

