"""
Day 17.01 - CrewAI Role-Based Agents.

This module defines the three CrewAI `Agent`s used in this demo: a
researcher, a coder, and a reviewer. Each agent has a role, a goal, and a
backstory that CrewAI uses to shape how the underlying LLM behaves when
that agent works on a task. This illustrates CrewAI's "role-based agent"
concept, where specialized agents collaborate on a shared goal.
"""

from crewai import Agent

from llm import llm

# The researcher agent: gathers/explains AI agent concepts.
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

