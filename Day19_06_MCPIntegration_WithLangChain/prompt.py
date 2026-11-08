"""
Day 19.06 - MCP Integration with LangChain.

This module defines a reusable chat prompt template. It sets a system
message that frames the model as an "AI agent engineering teacher" and
leaves a `{question}` placeholder for whatever the human asks, so other
scripts can format and send consistent prompts to the model.
"""

from langchain_core.prompts import ChatPromptTemplate  # Builds reusable, templated chat prompts (system + human turns).

# Define the system/human message pair; "{question}" is filled in later by callers.
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

