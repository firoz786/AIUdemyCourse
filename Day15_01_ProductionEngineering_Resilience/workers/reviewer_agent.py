"""
Day 15 - Production Engineering & Resilience: Reviewer Worker Agent.

This file demonstrates the quality-gate worker in the multi-agent pipeline:
given a task and generated code, it asks the LLM (via the resilient call_llm
wrapper) to review the solution and return a strict JSON verdict - either
"approved" or "needs_revision" with feedback. The manager uses this
structured result to decide whether to finish or send the code back to the
coding agent for another revision pass (bounded by MAX_REVISIONS).
"""

from llm import call_llm
import json


def review(
    task,
    code
):
    # Build a prompt asking the LLM to review the code and return strict JSON
    # so the manager can parse the decision programmatically.
    prompt = f"""
You are a Reviewer Agent.

Review the following Python solution.

Task:
{task}

Solution:
{code}

Check:

1. Correctness
2. Python syntax
3. Logic
4. Missing issues
5. Possible improvements

Return ONLY valid JSON.

Use exactly this format:

{{
    "status": "approved",
    "feedback": "The solution is correct."
}}

OR:

{{
    "status": "needs_revision",
    "feedback": "Explain what needs to be changed."
}}

Use "approved" only when the solution
is acceptable.

Use "needs_revision" when the solution
requires a correction.
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

    # Clean up whitespace before parsing the expected JSON response.
    result = response.strip()

    # Parse into a dict (e.g. {"status": ..., "feedback": ...}) for the
    # manager to inspect.
    return json.loads(result)

