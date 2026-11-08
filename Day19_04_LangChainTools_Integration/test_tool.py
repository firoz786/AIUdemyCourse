"""
Day 19.04 - LangChain Tools (Integration) - manual tool invocation test.

Manually calls a LangChain tool directly (bypassing any model/agent) to
confirm it works in isolation. LangChain tools expose an .invoke(...)
method that takes a dict of arguments, even for tools with no parameters.
"""

# Import the tool we want to manually verify.
from tools import current_time

# current_time takes no arguments, so we invoke it with an empty dict.
result = current_time.invoke({})

print(result)
