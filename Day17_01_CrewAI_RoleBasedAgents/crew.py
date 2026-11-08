"""
Day 17.01 - CrewAI Role-Based Agents.

This module assembles the three agents (researcher, coder, reviewer) and
their matching tasks into a single CrewAI `Crew`, using the `sequential`
process: each task runs one after another, in the order listed, with later
tasks able to use earlier tasks' output as context. This is CrewAI's
simplest collaboration style.
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


