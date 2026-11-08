"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph) - entry point.

This script is the runnable demo for the conditional-edges lesson. It
connects to the MCP tool server, discovers the available tools, builds the
LangGraph graph defined in `graph.py` (which uses conditional edges to loop
between "planner" and "tool" nodes until the task is finished), asks the
user for a request, runs the graph end-to-end, and prints the final state.
"""

import sys
import asyncio

from agent.mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from graph import build_graph


async def main():

    # Open the MCP client connection to the local tool server.
    client = await connect()

    # Ask the server which tools it exposes (e.g. current_time, roll_dice).
    tools = await discover_tools(
        client
    )

    print("\nAvailable Tools")
    print("----------------")

    # Show the user which tools the planner is allowed to choose from.
    for tool in tools:
        print(tool.name)

    # Build the LangGraph graph (nodes + fixed edges + conditional edges).
    graph = build_graph(
        tools,
        client
    )

    # Ask the user what they want; guard against Ctrl+C / EOF so the demo
    # exits cleanly instead of showing a raw traceback.
    try:
        user_request = input(
            "\nUser : "
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        await disconnect(client)
        sys.exit(0)

    # Starting state for the graph run: counters/history start empty and
    # the loop keeps running (via conditional edges) until "finished".
    initial_state = {
        "user_request": user_request,
        "current_step": 0,
        "max_steps": 5,
        "actions": [],
        "observations": [],
        "action": "",
        "finished": False,
        "final_answer": ""
    }

    # Run the graph from START to END, following whichever path the
    # conditional edges choose at each step.
    result = await graph.ainvoke(
        initial_state
    )

    print("\nFinal State")
    print("-----------")
    print(result)

    # Always close the MCP connection cleanly when done.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())


