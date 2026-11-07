from langchain.agents import create_agent

from model import model
from mcp_tools import client
from rag_tool import search_knowledge


async def create_agent_instance():

    mcp_tools = await client.get_tools()

    tools = mcp_tools + [
        search_knowledge
    ]

    return create_agent(
        model=model,
        tools=tools
    )

