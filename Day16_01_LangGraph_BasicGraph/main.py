"""
Day16_01 - LangGraph Basic Graph entry point.

This script is the runnable demo for the lesson: it connects to the MCP
tool server, discovers which tools are available, compiles the LangGraph
graph defined in graph.py, and then invokes that graph once with the
user's request as the initial state. It prints the tools discovered and
the final state returned by the graph so you can see how state flows
through a (very small) graph-based agent.
"""

import sys
# asyncio lets us run the async MCP client calls (connect/disconnect/etc).
import asyncio

# Helper functions to talk to the MCP tool server.
from agent.mcp_client import (
    connect,
    disconnect,
    discover_tools
)

# build_graph() assembles and compiles our single-node LangGraph graph.
from graph import build_graph


async def main():
    # Open a connection to the MCP server (starts/attaches the tool process).
    client = await connect()

    # Ask the server which tools it exposes (e.g. current_time, roll_dice).
    tools = await discover_tools(client)

    # Teaching aid: list the tools the planner will be able to choose from.
    print("\nAvailable Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    # Compile the LangGraph graph now that we know which tools exist.
    graph = build_graph(tools)

    # Ask the human for their request; Ctrl+C/EOF should exit cleanly
    # instead of crashing with a traceback.
    try:
        user_request = input("\nUser : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # The initial state dictionary matching the AgentState schema; this is
    # what gets passed into the graph and updated by each node.
    initial_state = {
        "user_request": user_request,
        "current_step": 0,
        "max_steps": 5,
        "actions": [],
        "observations": [],
        "finished": False,
        "final_answer": ""
    }

    # Run the compiled graph: START -> planner -> END, returning the final
    # (possibly updated) state dictionary.
    result = graph.invoke(
        initial_state
    )

    # Show what the graph produced after running through its nodes.
    print("\nFinal State")
    print("-----------")
    print(result)

    # Always close the MCP connection cleanly once we're done.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
