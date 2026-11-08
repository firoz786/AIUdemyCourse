"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Same researcher/coder/reviewer agent setup as Day 17.02 (with the
researcher able to call the MCP "current_time" tool), but here they are
orchestrated by a hierarchical crew with a separate manager LLM (see
crew.py) instead of running strictly in sequence.
"""

from crewai import Agent

from llm import llm

from mcp_tools import (
    mcp_current_time
)

# The researcher agent: can call the MCP "current_time" tool in addition to
# reasoning with the LLM.
researcher = Agent(
    role="AI Researcher",
    goal=(
        "Research AI agent concepts "
        "and provide accurate information."
    ),
    backstory=(
        "You are an AI researcher "
        "specialized in AI agents."
    ),
    llm=llm,
    tools=[
        mcp_current_time
    ],
    verbose=True
)

# The coder agent: turns the researcher's findings into working Python code.
coder = Agent(
    role="Python Developer",
    goal=(
        "Create clear and correct "
        "Python code based on research."
    ),
    backstory=(
        "You are an experienced Python "
        "developer who writes clean and "
        "practical code."
    ),
    llm=llm,
    verbose=True
)

# The reviewer agent: critiques the coder's output for correctness/quality.
reviewer = Agent(
    role="Code Reviewer",
    goal=(
        "Review generated code "
        "and identify problems."
    ),
    backstory=(
        "You are a senior Python reviewer "
        "focused on correctness and quality."
    ),
    llm=llm,
    verbose=True
)


