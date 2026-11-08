"""
Day 20.06 - Production Complete Agent API.

This module assembles the final LangChain agent used by the production
FastAPI service. It combines tools coming from an external MCP (Model
Context Protocol) server (time, dice, password tools) with a local
retrieval-augmented-generation (RAG) tool that searches a small knowledge
base. The resulting agent is what `main.py` calls on every `/chat` request.
"""

from langchain.agents import create_agent

from model import model
from mcp_tools import client
from rag_tool import search_knowledge


async def create_agent_instance():
    # MCP tools live in a separate process (server.py), so fetching them is
    # async: this talks to that server and gets back LangChain-compatible
    # tool wrappers (current_time, roll_dice, generate_password, etc).
    mcp_tools = await client.get_tools()

    # Combine the remote MCP tools with our local RAG tool so the agent can
    # choose whichever tool best answers the user's question.
    tools = mcp_tools + [
        search_knowledge
    ]

    # Build the actual LangChain agent, wiring in the chat model and the
    # full combined tool list.
    return create_agent(
        model=model,
        tools=tools
    )

