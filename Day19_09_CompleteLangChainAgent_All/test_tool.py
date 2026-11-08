"""
Day 19.09 - Quick manual test for a single LangChain tool.

This script is a tiny smoke test: it calls the `current_time` tool
(defined in tools.py) directly, outside of any agent, to confirm the
tool itself works and returns the expected value.
"""

from tools import current_time

# Invoke the tool directly with an empty input dict (it takes no arguments).
result = current_time.invoke({})

print(result)
