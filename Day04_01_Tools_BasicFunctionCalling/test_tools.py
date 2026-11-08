"""
Day04_01_Tools_BasicFunctionCalling: a quick manual smoke test that calls
each tool function once and prints the result, so you can see what each
tool actually returns before it gets wired into an LLM's tool-calling flow.
"""

from tools import get_current_time, roll_dice, generate_password

# Call each tool directly (no AI involved yet) and print its output.
print(get_current_time())
print(roll_dice())
print(generate_password())
