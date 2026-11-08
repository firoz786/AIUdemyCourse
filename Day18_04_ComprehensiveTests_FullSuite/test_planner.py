"""
Day 18.04 - Comprehensive Tests (Full Suite) - planner smoke test.

Manual behavior check for create_research_plan(): feeds it a sample
request and prints the resulting numbered research plan so you can
visually confirm it is sensible before trusting the full agent to
follow it.
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

