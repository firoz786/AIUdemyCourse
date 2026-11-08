"""
Day07_01_Planning_ChooseTool: a quick manual test that calls `choose_tool`
with a few different example requests, to see whether the AI planner picks
the right tool name (or "none") for each one.
"""

from planner import choose_tool

# Should pick "get_current_time".
print(
    choose_tool("What time is it?")
)

# Should pick "generate_password".
print(
    choose_tool("Generate a password")
)

# Should pick "roll_dice".
print(
    choose_tool("Roll a dice")
)

# Should pick "none" since no tool matches this request.
print(
    choose_tool("Explain Python")
)

