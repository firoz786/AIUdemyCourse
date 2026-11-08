"""
Day 19.02 - Prompt Templates (Parameterized Text) - reusable prompt.

Defines a ChatPromptTemplate: a reusable, parameterized sequence of chat
messages. It has a fixed "system" message that sets the AI's persona, and
a "human" message containing a {question} placeholder that gets filled in
differently each time the template is invoked.
"""

# ChatPromptTemplate builds a list of chat messages from a template.
from langchain_core.prompts import ChatPromptTemplate

# Build the template from a list of (role, text) message pairs. The
# "{question}" placeholder is filled in later via prompt.invoke(...).
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

