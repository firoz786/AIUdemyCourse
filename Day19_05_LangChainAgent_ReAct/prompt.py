"""
Day 19.05 - LangChain Agent (ReAct) - reusable prompt template.

Same parameterized prompt template as earlier days. It is kept here for
reference/reuse, though the ReAct agent in main.py is built directly
from the model and tools rather than from this prompt template.
"""

# ChatPromptTemplate builds a list of chat messages from a template.
from langchain_core.prompts import ChatPromptTemplate

# Build the template from a list of (role, text) message pairs. The
# "{question}" placeholder would be filled in when the template is invoked.
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

