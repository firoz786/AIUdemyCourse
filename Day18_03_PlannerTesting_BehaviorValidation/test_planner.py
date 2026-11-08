"""
Day 18.03 - Planner Testing (Behavior Validation) - planner smoke test.

Manual behavior-validation script for the new create_research_plan()
function: it feeds a sample request to the planner and prints the
resulting numbered plan, so you can visually confirm the plan looks
sensible and ordered before trusting the full agent to follow it.
"""

# Import just the planner function (not the whole agent loop).
from agent import create_research_plan

# A sample (deliberately slightly messy, with a stray tab character)
# research request to see how the planner handles it.
request = (
    "Research about the jobs requirement in AI 	agent domain."
)

# Ask the model to turn the request into an ordered research plan.
plan = create_research_plan(
    request
)


print("\nRESEARCH PLAN\n")
print(plan)

