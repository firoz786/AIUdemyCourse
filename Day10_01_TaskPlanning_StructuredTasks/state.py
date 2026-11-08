"""
Day10_01_TaskPlanning_StructuredTasks - state.py

This file extends the agent state concept from Day09 with explicit task
tracking: each sub-task has a status ("pending"/"completed"), and helper
functions let the loop add tasks, mark them complete (with tolerant text
matching), record actions/observations/results, and check whether the
whole plan is done. This richer state is what lets the Day10 loop reason
about multi-step plans instead of single actions.
"""


def create_state(user_request, max_steps=5):
    # Build the initial state dict: the original request, the list of
    # planned tasks (filled in later), which task is currently active, a
    # step counter/limit, and histories of actions/observations/results.
    return {
        "user_request": user_request,
        "tasks": [],
        "current_task": None,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "results": [],
        "finished": False,
        "final_answer": ""
    }


def add_task(state, task):
    # Register a new sub-task, starting out as "pending".
    state["tasks"].append({
        "task": task,
        "status": "pending"
    })


def complete_task(state, task):

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
    # Record that the agent decided to take this action (e.g. a tool name).
    state["actions"].append(action)


def record_observation(
    state,
    action,
    observation
):
    # Store what happened when `action` was executed, tagged with the step
    # number so the full reasoning trace can be replayed/inspected later.
    state["observations"].append({
        "step": state["current_step"],
        "action": action,
        "observation": observation
    })


def add_result(state, result):
    # Append an intermediate result/finding to the running results list.
    state["results"].append(result)


def get_pending_tasks(state):
    # Return just the task text for tasks that haven't been completed yet.
    return [
        item["task"]
        for item in state["tasks"]
        if item["status"] == "pending"
    ]


def all_tasks_completed(state):
    # No tasks at all counts as "not done" (the plan hasn't been built
    # yet); otherwise every task must have status "completed".
    if not state["tasks"]:
        return False

    return all(
        item["status"] == "completed"
        for item in state["tasks"]
    )


def next_step(state):
    # Advance the loop counter after completing one plan/act/observe cycle.
    state["current_step"] += 1


def can_continue(state):
    # The agent may keep looping only if it hasn't finished AND hasn't hit
    # the maximum allowed number of steps (prevents runaway loops).
    return (
        not state["finished"]
        and state["current_step"] < state["max_steps"]
    )


def finish(state, answer):
    # Mark the state as complete and store the final answer to show the user.
    state["final_answer"] = answer
    state["finished"] = True
