"""
Day 14.05 - Parallel Agents with Concurrency: Shared State
------------------------------------------------------------------
Same state shape as Day 14.04, including the `revision_count` used to cap
the coding/review loop. This folder's "what's new" is concurrency, shown
separately in parallel_demo.py rather than in this state module.
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
