"""
Day 17.02 - CrewAI with MCP Tool Integration.

Assembles the researcher/coder/reviewer agents and their tasks into a
sequential `Crew`, just like Day 17.01, except the researcher here has
access to a real MCP-backed tool (see agents.py / mcp_tools.py).
"""

from crewai import Crew, Process

from agents import (
    researcher,
    coder,
    reviewer
)

from tasks import (
    research_task,
    coding_task,
    review_task
)

# The crew ties agents + tasks together and runs them one after another
# (Process.sequential), passing each task's output along as context.
crew = Crew(
    agents=[
        researcher,
        coder,
        reviewer
    ],
    tasks=[
        research_task,
        coding_task,
        review_task
    ],
    process=Process.sequential,
    verbose=True
)


