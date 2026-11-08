"""
Day 19.04 - LangChain Tools (Integration) - chain with prompt + model.

Reuses the same prompt | model | parser chain from Day 19.03 as a
reminder of chain composition. The actual tool-integration demo for this
folder lives in test_tool.py and tools.py, which show how to define and
directly invoke a LangChain @tool-decorated function.
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
