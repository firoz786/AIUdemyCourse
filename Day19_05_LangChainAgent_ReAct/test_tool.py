"""
Day 19.05 - LangChain Agent (ReAct) - manual tool invocation test.

Manually calls a LangChain tool directly (bypassing the agent) to confirm
it works in isolation, before trusting the ReAct agent in main.py to call
it automatically.
"""

# Import the tool we want to manually verify.
from tools import current_time

# current_time takes no arguments, so we invoke it with an empty dict.
result = current_time.invoke({})

print(result)
