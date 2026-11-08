"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This script is the entry point for the human-in-the-loop demo: it connects
to an MCP tool server, builds the LangGraph agent graph, and then drives the
conversation loop. Whenever the graph hits an `interrupt()` (i.e. it wants
human approval before running a tool), this script prints the pending
action, asks the user to approve or reject it via `input()`, and resumes the
graph with the `Command(resume=...)` API until the agent finishes.
"""

import sys
import asyncio

# Command lets us resume a paused (interrupted) graph with a human's decision.
from langgraph.types import Command

from agent.mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from graph import build_graph


async def main():

    # Open the MCP client connection to the local tool server.
    client = await connect()

    try:

        # Ask the MCP server which tools it exposes (e.g. current_time, roll_dice).
        tools = await discover_tools(client)

        print("\nAvailable Tools")
        print("----------------")

        for tool in tools:
            print(tool.name)

        # Build the compiled LangGraph (planner -> approval -> tool -> answer).
        graph = build_graph(tools, client)

        # Ask the user what they want the agent to do. Wrapped so Ctrl+C
        # (or closing stdin) exits cleanly instead of crashing with a traceback.
        try:
            user_request = input("\nUser : ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
            sys.exit(0)

        # The shared state that flows through every node of the graph.
        initial_state = {
            "user_request": user_request,
            "current_step": 0,
            "max_steps": 5,
            "actions": [],
            "observations": [],
            "action": "",
            "approval": "",
            "finished": False,
            "final_answer": ""
        }

        # thread_id identifies this conversation to the checkpointer, so the
        # graph can be paused/resumed across multiple ainvoke() calls.
        config = {
            "configurable": {
                "thread_id": "demo-1"
            }
        }

        # Kick off the graph. It will run until it finishes or hits an interrupt().
        result = await graph.ainvoke(initial_state, config)

        # Keep resuming the graph every time it pauses for human approval,
        # until it reports no more interrupts (i.e. it has finished).
        while True:

            interrupts = result.get("__interrupt__")

            if not interrupts:
                break

            # Show the human what tool the agent wants to run and why.
            interrupt_data = interrupts[0].value

            print("\n==============================")
            print(" HUMAN APPROVAL REQUIRED")
            print("==============================")
            print(interrupt_data["message"])
            print("Tool:", interrupt_data["action"])

            # Ask for approval. Wrapped so Ctrl+C exits the loop gracefully
            # instead of raising an unhandled exception mid-conversation.
            try:
                decision = input("\nApprove? (yes/no): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
                break

            # Resume the paused graph, feeding the human's decision back in
            # as the result of the interrupt() call.
            result = await graph.ainvoke(Command(resume=decision), config)

        print("\nFinal State")
        print("-----------")
        print(result)

    finally:
        # Always close the MCP connection, even if something above failed.
        await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
