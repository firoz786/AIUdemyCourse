"""
Day 17.01 - CrewAI Role-Based Agents.

Defines the three `Task`s that drive the sequential crew: research the
agent concept, write example code based on that research, and review the
code. Each task is assigned to a specific agent, and later tasks declare
earlier tasks as `context` so CrewAI passes their output along automatically.
"""

from crewai import Task

from agents import (
    researcher,
    coder,
    reviewer
)

# Step 1: the researcher explains the core AI agent concepts.
research_task = Task(
    description=(
        "Research the concept of "
        "autonomous AI agents. "
        "Explain the agent loop, "
        "tools, state and observations."
    ),
    expected_output=(
        "A concise technical explanation "
        "of autonomous AI agents."
    ),
    agent=researcher
)

# Step 2: the coder writes example code, using the research as context.
coding_task = Task(
    description=(
        "Using the research provided by "
        "the researcher, create a simple "
        "Python example of an AI agent loop."
    ),
    expected_output=(
        "A complete Python code example "
        "with a short explanation."
    ),
    agent=coder,
    context=[
        research_task
    ]
)

# Step 3: the reviewer critiques the code, using the coding task as context.
review_task = Task(
    description=(
        "Review the Python code produced "
        "by the developer. Identify "
        "errors and suggest improvements."
    ),
    expected_output=(
        "A code review containing "
        "identified problems and "
        "recommended improvements."
    ),
    agent=reviewer,
    context=[
        coding_task
    ]
)

