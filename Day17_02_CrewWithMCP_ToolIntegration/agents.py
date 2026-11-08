"""
Day 17.02 - CrewAI with MCP Tool Integration.

This module defines the same three role-based agents as Day 17.01
(researcher, coder, reviewer), but the researcher is additionally given a
CrewAI `tool` (`mcp_current_time`) that is backed by a real MCP server. This
demonstrates how CrewAI agents can call out to external tools exposed over
the Model Context Protocol, not just rely on the LLM's own knowledge.
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


