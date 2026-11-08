"""
Day 20.06 - Production Complete Agent API.

Defines the `search_knowledge` tool: a retrieval-augmented-generation (RAG)
tool that lets the agent search a small local knowledge base (built from
notes.txt via retriever.py) and get back the most relevant text snippets to
help answer the user's question.
"""

from langchain_core.tools import tool

from retriever import retriever


@tool
def search_knowledge(question: str) -> str:
    """Search the local knowledge base and return relevant information."""

    # Ask the vector store retriever for the documents most similar to the
    # question (semantic search over the embedded notes.txt chunks).
    documents = retriever.invoke(question)

    # Join each matching chunk's text together so the agent gets one
    # combined block of context to reason over.
    return "\n\n".join(
        document.page_content
        for document in documents
    )


