"""
Day 19.08 - Memory with LangChain (Conversation).

This module defines a reusable chat prompt template used by the shared
agent demo (main.py). It sets a system message that frames the model as an
"AI agent engineering teacher" and leaves a `{question}` placeholder for
whatever the human asks.
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

