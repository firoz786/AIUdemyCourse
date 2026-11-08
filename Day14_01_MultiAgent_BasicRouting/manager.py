"""
Day 14.01 - Multi-Agent Basic Routing: Manager
--------------------------------------------------
This is the "Manager" that coordinates the multi-agent system. Unlike later
days, routing here is hardcoded: the manager always calls the Research
Agent, then the Coding Agent, then the Reviewer Agent, in that fixed order,
and returns all three results together. There is no dynamic decision-making
yet - that is introduced in Day 14.02 with an LLM-based router.
"""

# Import the three worker agents this manager coordinates.
from research_agent import research
from coding_agent import write_code
from reviewer_agent import review


def run_manager(task):
    # Step 1: ask the Research Agent to gather background info for the task.
    print("\nManager → Research Agent")

    research_result = research(
        task
    )

    # Step 2: ask the Coding Agent to write code using the task + research.
    print("\nManager → Coding Agent")

    code_result = write_code(
        task,
        research_result
    )

    # Step 3: ask the Reviewer Agent to critique the generated code.
    print("\nManager → Reviewer Agent")

    review_result = review(
        task,
        code_result
    )

    # Bundle all three outputs into one dictionary so main.py can display them.
    return {
        "research": research_result,
        "code": code_result,
        "review": review_result
    }
