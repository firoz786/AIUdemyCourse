"""
Day 18.03 - Planner Testing (Behavior Validation) - agent smoke test.

Manual integration test: runs the full research_agent loop on a sample
request and prints its final answer, confirming the agent still behaves
correctly after the planner was added to agent.py.
"""

# Import the agent entry point we want to exercise end-to-end.
from agent import research_agent

# A sample research request to drive the agent with.
request = """
Search the web for the latest Jobs in AI agents
Domain and explain the five most important skill requirements.
"""

# Run the agent - this will loop internally, calling tools as needed.
answer = research_agent(
    request
)


print("\nFINAL ANSWER\n")
print(answer)

