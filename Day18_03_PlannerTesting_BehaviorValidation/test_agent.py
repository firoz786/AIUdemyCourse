from agent import research_agent


request = """
Search the web for the latest Jobs in AI agents
Domain and explain the five most important skill requirements.
"""

answer = research_agent(
    request
)


print("\nFINAL ANSWER\n")
print(answer)

