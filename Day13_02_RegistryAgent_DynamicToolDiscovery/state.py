"""
Day13_02 - Registry Agent: Dynamic Tool Discovery
===================================================
This module defines the plain-dictionary "state" object the agent loop
threads through every iteration: the original request, how many steps
have run, which actions were taken, what was observed, and whether the
agent is finished. Keeping state as simple functions over a dict (no
classes) keeps the agent loop easy to follow for beginners.
"""


def create_state(user_request, max_steps=5):
    """Build a fresh agent state for a new user request."""
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
    """Record that this action was chosen/performed."""
    state["actions"].append(action)


def record_observation(state, action, observation):
    """Record what happened when `action` was executed."""
    state["observations"].append({
        "step": state["current_step"],
        "action": action,
        "observation": observation
    })


def next_step(state):
    """Advance the step counter after one plan/act/observe cycle."""
    state["current_step"] += 1


def can_continue(state):
    """True while the agent hasn't finished and hasn't hit the step limit."""
    return (
        not state["finished"]
        and state["current_step"] < state["max_steps"]
    )


def finish(state, answer):
    """Mark the agent as done and store its final answer."""
    state["final_answer"] = answer
    state["finished"] = True
