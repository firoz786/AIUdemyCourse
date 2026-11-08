"""
Day 19.09 - Reusable chat prompt template.

This module defines a simple two-message prompt template (a system
message that sets the agent's persona, plus a human message that will be
filled in with the user's question). It is a small, standalone example of
`ChatPromptTemplate.from_messages` and is not wired into the other
scripts in this folder.
"""

from langchain_core.prompts import ChatPromptTemplate

# Build a reusable prompt: the "system" message fixes the agent's
# persona, and "{question}" is a placeholder filled in at call time.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI agent engineering teacher."
        ),
        (
            "human",
            "{question}"
        )
    ]
)

