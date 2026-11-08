"""
Day 15 - Production Engineering & Resilience: Input Validation.

This file demonstrates the "validation" pillar of resilience: before the
agent system spends time and LLM calls on a user-supplied task, it checks
that the input is actually usable (not empty, not absurdly long). Rejecting
bad input early with a clear ValueError prevents wasted work and confusing
downstream failures deeper in the pipeline.
"""


def validate_task(task):
    # Reject empty/falsy input (None, "", etc.) right away.
    if not task:

        raise ValueError(
            "Task cannot be empty."
        )

    # Remove leading/trailing whitespace so later checks/usage are clean.
    task = task.strip()

    # Guard against unreasonably long input that could blow up token limits
    # or indicate a mistake/abuse.
    if len(task) > 5000:

        raise ValueError(
            "Task is too long."
        )

    return task
