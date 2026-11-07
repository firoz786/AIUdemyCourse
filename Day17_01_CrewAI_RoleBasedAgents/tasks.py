from crewai import Task

from agents import (
    researcher,
    coder,
    reviewer
)


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

