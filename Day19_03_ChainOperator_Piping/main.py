"""
Day 19.03 - Chain Operator (Piping) - composing a chain with `|`.

Demonstrates LangChain's "LCEL" pipe operator: `prompt | model | parser`
builds a single chain object that runs the prompt template, feeds its
output to the chat model, and feeds the model's response through an
output parser that extracts plain text. Chaining with `|` avoids manually
calling .invoke() on each piece one after another.
"""

from model import model
from prompt import prompt
# StrOutputParser converts the model's response object into a plain string.
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

# The `|` operator composes prompt -> model -> parser into one runnable
# chain: data flows left to right through each step.
chain = (
    prompt
    | model
    | parser
)

# Run the whole chain in one call, filling in the prompt's {question}.
response = chain.invoke(
    {
        "question": "Why is MCP useful for AI agents?"
    }
)

# Thanks to StrOutputParser, response is already a plain string here.
print(response)
