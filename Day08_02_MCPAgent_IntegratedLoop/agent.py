"""
Day08_02_MCPAgent_IntegratedLoop

This file demonstrates how an AI agent script connects to a running MCP
(Model Context Protocol) server and discovers the tools that server exposes.
MCP is like a "USB port" that lets an LLM-based agent plug into external
tools (such as a dice roller or password generator) without hard-coding
their logic into the agent itself. This script wires together an
OpenAI-compatible client with our own `mcp_client` helper module: it
connects to the server, lists the available tools, prints them, and then
disconnects cleanly.
"""

import asyncio

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (e.g. BASE_URL, API_KEY) from a local .env file.
load_dotenv()

# Create the AI client used to talk to the LLM provider.
# (Set up here as part of the agent's standard initialization pattern,
# even though this particular script only exercises tool discovery.)
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Import our own helper functions that wrap the MCP client lifecycle.
from mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool
)


async def main():
    # Step 1: Connect to the MCP Server.
    client = await connect()

    # Step 2: Discover all available tools exposed by the server.
    tools = await discover_tools(
        client
    )
    print()
    print("Available Tools")
    print("----------------")

    # Print just the tool names so the learner can see what the agent "sees".
    for tool in tools:
        print(tool.name)
    print()

    # Step 3: Always disconnect cleanly to release the MCP session.
    await disconnect(
        client
    )

if __name__ == "__main__":
    # Entry point: run the async main() coroutine using asyncio's event loop.
    asyncio.run(main())


