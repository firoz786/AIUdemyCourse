"""
Day 15 - Production Engineering & Resilience: Shared Agent State.

This file demonstrates keeping a single, explicit "state" dictionary that
flows through the whole multi-agent workflow (manager, research, coding,
review). Centralizing state like this makes the system easier to reason
about, debug, and log - every worker reads and writes a known set of fields
instead of passing around loose variables.
"""


def create_state(task):
    # Build the initial shared state for a new task: nothing has been
    # researched, coded, or reviewed yet, and no revisions have happened.
    return {
        "task": task,
        "research": "",
        "code": "",
        "review": "",
        "history": [],
        "revision_count": 0
    }
