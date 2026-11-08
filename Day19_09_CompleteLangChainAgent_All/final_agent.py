"""
Day 19.09 - Complete LangChain Agent (capstone).

This is the capstone script for the LangChain section of the course: it
combines everything learned in Day19_01 through Day19_08 into a single
agent. The agent gets tools from an MCP server (time/dice/password tools),
gets an extra local "search_knowledge" tool backed by a RAG retriever
(semantic search over notes.txt), and uses `create_agent` to let the LLM
decide which tool to call. Run it directly to ask one hard-coded question
and print the agent's final answer.
"""

import asyncio

from langchain.agents import create_agent
from langchain_core.tools import tool

from model import model
from mcp_tools import client
from retriever import retriever


@tool
def search_knowledge(question: str) -> str:
    """Search the local knowledge base and return relevant information."""

    # Ask the FAISS retriever for the chunks most similar to the question.
    documents = retriever.invoke(question)

    # Merge the retrieved chunks into one block of text for the LLM to read.
    return "\n\n".join(
        document.page_content
        for document in documents
    )


async def main():
    # Fetch the tools exposed by the MCP server (time, dice, password, etc.).
    mcp_tools = await client.get_tools()

    # Combine MCP tools with our local RAG-powered tool into one tool list.
    tools = mcp_tools + [
        search_knowledge
    ]

    # Build the agent: it can reason, call any of the tools above, and
    # decide on its own which one(s) to use to answer the user's question.
    agent = create_agent(
        model=model,
        tools=tools
    )

    # Send a single user question through the agent (async, since MCP and
    # the agent both use async I/O under the hood).
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "According to my notes, what is MCP?"
                }
            ]
        }
    )

    # The agent returns the full conversation; the last message is the answer.
    print("\nFINAL ANSWER")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    # Entry point: run the async main() function using asyncio's event loop.
    asyncio.run(main())

