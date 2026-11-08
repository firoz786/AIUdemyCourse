"""
Day 19.04 - LangChain Tools (Integration) - reusable prompt template.

Same parameterized prompt template as earlier days; used by the chain in
main.py.
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

