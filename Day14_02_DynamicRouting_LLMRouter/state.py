"""
Day 14.02 - Dynamic Routing with an LLM Router: Shared State
------------------------------------------------------------------
This tiny module defines the shape of the "state" dictionary that is
passed between the Manager and all worker agents. Keeping shared state in
one place (instead of scattering loose variables) is what makes it
possible for the Manager to dynamically decide what to do next: it can
look at which fields are still empty and route accordingly.
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
