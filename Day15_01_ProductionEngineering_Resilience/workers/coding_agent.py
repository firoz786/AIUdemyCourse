"""
Day 15 - Production Engineering & Resilience: Coding Worker Agent.

This file demonstrates a single-purpose "worker" agent that the manager
delegates to: given a task, prior research, and optional reviewer feedback,
it asks the LLM (via the resilient call_llm wrapper with retry/backoff) to
write or revise Python code. Keeping this worker focused on one job makes
the overall multi-agent system easier to test, permission-scope, and reason
about than one giant do-everything agent.
"""

from llm import call_llm


def write_code(
    task,
    research,
    feedback=""
):
    # Build a prompt giving the LLM the task, research context, and any
    # feedback from a previous review so it can fix known issues.
    prompt = f"""
You are a Coding Agent.

Write or revise Python code based on
the task and research.

Task:
{task}

Research:
{research}

Previous Reviewer Feedback:
{feedback}

If reviewer feedback is provided,
correct the identified problems.

Return:

1. Short explanation
2. Complete Python code
"""

    # Delegate to the shared, retrying LLM caller.
    response = call_llm(
            messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response

