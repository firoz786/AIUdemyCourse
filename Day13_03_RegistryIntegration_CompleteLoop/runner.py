"""
Day13_03 - Registry Integration: The Complete Loop
====================================================
This is the entry point for Day13_03, the final step in the Day13
MCP registry progression. It is almost identical to Day13_02's agent
loop, but the weather tool is no longer launched as a local script -
it now lives on a separate, already-running MCP server reached over
HTTP. This demonstrates that the registry pattern doesn't care whether
a tool comes from a local stdio process or a remote network server; it
discovers and calls tools identically either way.
"""
import asyncio
import os
import sys

from openai import OpenAI
from dotenv import load_dotenv

from mcp_manager import create_tool_registry, close_servers
from planner import planner
from executor import execute_action
from loop import run_agent_loop

# The time server is still a local script (stdio transport), while the
# weather server has moved to a remote HTTP endpoint - start it
# separately first (e.g. `python weather-mcp-server/server.py`).
servers = [
    "time-mcp-server/server.py",
    # "weather-mcp-server/server.py"  # old local-script target, replaced below
    "http://127.0.0.1:8000/mcp"
]

# Load API credentials/config (BASE_URL, API_KEY, MODEL) from a .env file.
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def format_answer(state):
    """Ask the LLM to turn the raw actions/observations into a natural reply."""
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
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


async def main():
    # Connect to both servers (one local stdio, one remote HTTP) and
    # build one combined tool registry.
    clients, tool_registry = await create_tool_registry(servers)

    # client = await connect()
    # tools = await discover_tools(client)

    # Pull the raw tool objects out of the registry for the planner prompt.
    tools = [entry["tool"] for entry in tool_registry.values()]

    print()
    print("Available Tools")
    print("----------------")
    for tool in tools:
        print(tool.name)

    try:
        # Ask the user what they want the agent to do; Ctrl+C/Ctrl+D
        # should exit cleanly instead of raising a traceback.
        user_request = input("\nUser : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        await close_servers(clients)
        sys.exit(0)

    # Run the full plan -> act -> observe loop until FINISH or step limit.
    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        tool_registry
    )

    print()
    print("Final Answer:")
    print(state["final_answer"])

    await close_servers(clients)


if __name__ == "__main__":
    asyncio.run(main())
