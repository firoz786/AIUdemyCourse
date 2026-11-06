import asyncio

from langchain.agents import create_agent
from langchain_core.tools import tool

from model import model
from mcp_tools import client
from retriever import retriever


@tool
def search_knowledge(question: str) -> str:
    """Search the local knowledge base and return relevant information."""

    documents = retriever.invoke(question)

    return "\n\n".join(
        document.page_content
        for document in documents
    )


