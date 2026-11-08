"""
Day 17.02 - CrewAI with MCP Tool Integration.

Defines the three tasks for the sequential crew. The research task now
explicitly instructs the researcher agent to call the MCP "Current Time"
tool before finishing, so the final output includes a real timestamp
fetched via MCP rather than one the LLM makes up.
"""

from crewai import Task

from agents import (
    researcher,
    coder,
    reviewer
)

# Step 1: the researcher explains AI agent concepts AND must call the MCP
# current-time tool, proving the tool integration actually happened.
research_task = Task(
    description=(
        "Research autonomous AI agents. "
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


