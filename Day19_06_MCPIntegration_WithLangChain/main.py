"""
Day 19.06 - MCP Integration with LangChain.

This script demonstrates how a LangChain agent can use tools that live on a
separate MCP (Model Context Protocol) server process, instead of tools defined
directly in Python. It starts the MCP client, asks it for the available
tools, builds a LangChain agent around those tools and a chat model, and then
asks the agent a question that requires calling one of the remote MCP tools.
"""

import asyncio  # Lets us run the async agent code with asyncio.run().

from langchain.agents import create_agent  # Helper that builds a tool-using LangChain agent.

from model import model  # The chat model (ChatOllama) the agent will reason with.
from mcp_tools import client  # The MCP client configured to talk to our MCP "time_server".


async def main():
    # Ask the MCP client to discover and wrap the server's tools as LangChain tools.
    tools = await client.get_tools()

    # Create an agent that can decide when to call the MCP tools to answer questions.
    agent = create_agent(
        model=model,
        tools=tools
    )

    # Send a user question to the agent; it will call the MCP "current_time" tool if needed.
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

    # Print just the final assistant message, which is the agent's answer.
    print("\nFINAL ANSWER")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    # Entry point: run the async main() coroutine to completion.
    asyncio.run(main())

