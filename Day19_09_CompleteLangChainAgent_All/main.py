"""
Day 19.09 - Complete LangChain Agent (MCP tools only, warm-up script).

This is a smaller companion to final_agent.py: it shows the minimal setup
needed to connect a LangChain agent to tools exposed by an MCP server
(see mcp_tools.py / server.py), without the extra RAG "search_knowledge"
tool. Run it directly to ask one hard-coded question and print the
agent's final answer.
"""

import asyncio

from langchain.agents import create_agent

from model import model
from mcp_tools import client


async def main():
    # Ask the MCP client to discover all tools the MCP server exposes
    # (e.g. current_time, roll_dice, generate_password).
    tools = await client.get_tools()

    # Build the agent, giving it access to every MCP tool we just fetched.
    agent = create_agent(
        model=model,
        tools=tools
    )

    # Send a single user question through the agent and await the result.
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the current time?"
                }
            ]
        }
    )

    # The last message in the conversation is the agent's final answer.
    print("\nFINAL ANSWER")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    # Entry point: run the async main() function using asyncio's event loop.
    asyncio.run(main())

