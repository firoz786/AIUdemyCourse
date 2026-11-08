"""
Day 19.07 - RAG with LangChain (Retrieval).

Small standalone script to sanity-check the `current_time` LangChain tool
in isolation (without an agent or MCP server), by invoking it directly and
printing the result.
"""

from tools import current_time  # Import the LangChain-wrapped tool function to test.

# Call the tool directly with an empty input dict (it takes no arguments).
result = current_time.invoke({})

print(result)
