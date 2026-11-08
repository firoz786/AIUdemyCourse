"""
Day 11.3 - Memory Extraction & Context Awareness.

This module defines the shared "state" dictionary that flows through the
whole agent loop, plus small helper functions to read and update it. The
state tracks the user's request, the task list, actions taken, tool
observations, intermediate results, and the relevant long-term memories
retrieved for this conversation.
"""


def create_state(user_request, max_steps=5):
    """Build a fresh state dict for a brand-new user request."""

    return {
        "user_request": user_request,
        "tasks": [],
        "current_task": None,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "results": [],
        "memories": [],
        "finished": False,
        "final_answer": ""
    }


def add_memory(state, memory):
    """Attach one retrieved long-term memory to the current state."""
    state["memories"].append(memory)


def add_task(state, task):
    """Add a new task (starting as "pending") to the task list."""

    state["tasks"].append({
        "task": task,
        "status": "pending"
    })


def complete_task(state, task):
    """Mark the task matching `task` as completed, tolerating minor
    wording differences between the planner's text and the stored task."""

    # Normalize the task received from the planner.
    # This makes the comparison tolerant of:
    # "Generate password"
    # "generate password"
    # "generate_password"

    normalized_task = (
        task
        .strip()
        .lower()
        .replace("_", " ")
    )

    for item in state["tasks"]:

        normalized_existing_task = (
            item["task"]
            .strip()
            .lower()
            .replace("_", " ")
        )

        if normalized_existing_task == normalized_task:

            item["status"] = "completed"

            return True

    return False


def add_action(state, action):
    """Record that a tool/action was invoked during this loop."""

    state["actions"].append(action)


def record_observation(
    state,
    action,
    observation
):
    """Save what happened when `action` was run, tagged with the step number."""

    state["observations"].append({
        "step": state["current_step"],
        "action": action,
        "observation": observation
    })


def add_result(state, result):
    """Append a result/outcome string to the running results list."""

    state["results"].append(result)


def get_pending_tasks(state):
    """Return the list of task descriptions still marked as pending."""

    return [
        item["task"]
        for item in state["tasks"]
        if item["status"] == "pending"
    ]


def all_tasks_completed(state):
    """True only if there is at least one task and every task is completed."""

    if not state["tasks"]:
        return False

    return all(
        item["status"] == "completed"
        for item in state["tasks"]
    )


def next_step(state):
    """Advance the step counter after finishing one loop iteration."""

    state["current_step"] += 1


def can_continue(state):
    """True while the agent hasn't finished and hasn't hit the step limit."""

    return (
        not state["finished"]
        and state["current_step"] < state["max_steps"]
    )


def finish(state, answer):
    """Store the final answer and mark the agent loop as finished."""

    state["final_answer"] = answer
    state["finished"] = True
