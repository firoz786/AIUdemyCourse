"""
Day 14.03 - Review Loop with Structured Feedback: Shared State
------------------------------------------------------------------
Defines the shape of the state dictionary shared between the Manager and
the worker agents. Still the same fields as Day 14.02 - the revision
counter used to cap how many times we loop back to the Coding Agent is
only added in Day 14.04.
"""


def create_state(task):
    # Build the starting state for a new run: the original task plus empty
    # placeholders for each worker's output, and a history log of steps taken.
    return {
        "task": task,
        "research": "",
        "code": "",
        "review": "",
        "history": []
    }
