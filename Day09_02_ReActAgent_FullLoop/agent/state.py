"""
Day09_02_ReActAgent_FullLoop - agent/state.py

This file defines the same agent state data structure introduced in
Day09_01, re-used here as the backbone of the full ReAct loop (loop.py).
It provides small helper functions to create a fresh state, record
actions/observations, advance the step counter, check whether the loop
should keep going, and mark the run as finished with a final answer.
"""


def create_state(user_request, max_steps=5):
    # Build the initial state dict for a brand-new agent run: the original
    # request, a step counter, a step limit (safety net against infinite
    # loops), empty histories of actions/observations, and a "not finished
    # yet" flag with an empty final answer.
    return {
        "user_request": user_request,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "finished": False,
        "final_answer": ""
    }


def add_action(state, action):
    # Record that the agent decided to take this action (e.g. a tool name).
    state["actions"].append(action)


def record_observation(state, action, observation):
    # Store what happened when `action` was executed, tagged with the step
    # number so the full reasoning trace can be replayed/inspected later.
    state["observations"].append(
        {
            "step": state["current_step"],
            "action": action,
            "observation": observation
        }
    )


def next_step(state):
    # Advance the loop counter after completing one think/act/observe cycle.
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

