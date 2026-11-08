"""
Day 14.04 - Review Iteration with Refinement: Shared State
------------------------------------------------------------------
What's NEW in this file compared to Day 14.03: the state now tracks
`revision_count`, how many times the Coding Agent has revised its answer.
The Manager (see manager.py) uses this counter together with a
MAX_REVISIONS limit to stop an infinite back-and-forth between the Coding
Agent and the Reviewer Agent.
"""


def create_state(task):
    # Build the starting state for a new run: the original task, empty
    # placeholders for each worker's output, a history log, and a revision
    # counter that starts at zero (no revisions have happened yet).
    return {
        "task": task,
        "research": "",
        "code": "",
        "review": "",
        "history": [],
        "revision_count": 0
    }
