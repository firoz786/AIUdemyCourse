"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Defines the tasks used by both crews in crew.py. The first three tasks
mirror Day 17.02 (research -> code -> review), with the research task also
injecting a line asking the agent to remember the user's name - this is
what the `memory_task` later tries to recall, demonstrating CrewAI's
long-term memory feature.
"""

from crewai import Task

from agents import (
    researcher,
    coder,
    reviewer
)

# Step 1: the researcher explains AI agent concepts, calls the MCP
# current-time tool, and is told a name to remember (used by memory_task).
research_task = Task(
    description=(
        "Hi. I am Pankaj Shukla.Remember that my name is Pankaj Shukla for future interactions."" Research autonomous AI agents. "
        "Explain the agent loop, tools, "
        "state and observations. "
        "Before completing the task, use "
        "the MCP Current Time tool and "
        "include the returned time."
    ),
    expected_output=(
        "A concise technical explanation "
        "including the current time "
        "obtained from the MCP tool."
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

# A separate task (used by memory_crew in crew.py) that asks the researcher
# to recall the name from research_task, purely to prove memory persists.
memory_task = Task(
    description=(
        "What is the name of the person who "
        "introduced himself in our previous task?"
    ),
    expected_output=(
        "The name of the person."
    ),
    agent=researcher
)


