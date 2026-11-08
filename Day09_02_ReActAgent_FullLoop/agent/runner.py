"""
Day09_02_ReActAgent_FullLoop - agent/runner.py

This is the entry point that wires the whole ReAct agent together: it
connects to the MCP server, discovers the available tools, reads a request
from the user, runs the full think/act/observe loop (run_agent_loop) until
the agent decides it's done, and prints the final natural-language answer.
This is the file you actually run to see Day09_02's ReAct loop in action.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
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


# Load environment variables (e.g. BASE_URL, API_KEY, MODEL) from .env.
load_dotenv()

# Create the AI client used to turn the final state into a natural reply.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    # Ask the LLM to summarize everything the agent did into one natural,
    # user-facing answer, without leaking internal planning details.
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
    # Step 1: Connect to the MCP Server.
    client = await connect()

    # Step 2: Discover all available tools exposed by the server.
    tools = await discover_tools(client)

    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    # Step 3: Ask the user what they want. Wrapped in try/except so that
    # Ctrl+C (KeyboardInterrupt) or an unexpected end-of-input (EOFError)
    # exits the program gracefully instead of printing a scary traceback.
    try:
        user_request = input("\nUser : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # Step 4: Run the full ReAct loop (reason -> act -> observe -> repeat)
    # until the agent finishes or runs out of steps.
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

    # Step 5: Always disconnect cleanly from the MCP server.
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())

