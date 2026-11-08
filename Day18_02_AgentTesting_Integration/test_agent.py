"""
Day 18.02 - Agent Testing (Integration) - manual end-to-end agent test.

This script is a manual integration test: it runs the full research_agent
loop (LLM + tools together) on a sample request and prints the final
answer, letting you visually confirm the whole pipeline works together
(as opposed to unit-testing the tools or the model in isolation).
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

