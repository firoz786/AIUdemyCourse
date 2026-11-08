"""
Day 19.03 - Chain Operator (Piping) - reusable prompt template.

Same parameterized prompt template as Day 19.02; this is the first piece
piped together with `|` in main.py (prompt | model | parser).
"""

# ChatPromptTemplate builds a list of chat messages from a template.
from langchain_core.prompts import ChatPromptTemplate

# Build the template from a list of (role, text) message pairs. The
# "{question}" placeholder is filled in later when the chain is invoked.
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

