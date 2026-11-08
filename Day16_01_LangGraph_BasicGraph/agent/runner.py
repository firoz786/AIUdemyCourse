"""
Day16_01 - LangGraph Basic Graph: standalone plain-Python runner.

This script mirrors main.py but uses the plain Python agent loop
(loop.py) instead of the LangGraph graph, so you can compare "agent logic
as a while-loop" versus "agent logic as a graph". It connects to the MCP
server, discovers tools, asks the user for a request, runs the plan/act/
observe loop until finished, and prints the final natural-language answer.
"""

import os
import sys
import asyncio

from openai import OpenAI
from dotenv import load_dotenv

# MCP connection helpers (connect/disconnect/discover tools).
from mcp_client import (
    connect,
    disconnect,
    discover_tools
)

# The planner (decides next action), executor (runs the action), and the
# plain Python agent loop that ties them together.
from planner import planner
from executor import execute_action
from loop import run_agent_loop


load_dotenv()

# A shared OpenAI-compatible client used to turn the final state into a
# natural-language answer for the user.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    # Build a prompt that asks the LLM to phrase a friendly answer based on
    # what actions were performed and what was observed, without leaking
    # internal planning details to the user.
    prompt = f"""
The user asked:

{state["user_request"]}

Actions performed:

{state["actions"]}

Observations:

{state["observations"]}

Answer the user naturally.

Do not mention internal planning.
Do not mention state.
Do not mention tools.
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


async def main():
    # Open the MCP connection and see which tools are available.
    client = await connect()

    tools = await discover_tools(client)

    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    # Ask the human for their request; handle Ctrl+C/EOF gracefully instead
    # of letting the exception propagate as a traceback.
    try:
        user_request = input("\nUser : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # Run the plan -> act -> observe loop until the planner says FINISH.
    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        client
    )

    print()
    print("Final Answer:")
    print(state["final_answer"])

    # Always close the MCP connection cleanly once we're done.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
