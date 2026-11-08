"""
Day16_01 - LangGraph Basic Graph: plain Python agent loop (reference).

This module shows the "plan -> act -> observe" loop in plain Python,
without LangGraph, so you can compare it to the graph-based version in
graph.py. On each iteration it asks the planner what to do next, executes
that action via MCP, records the observation, and repeats until the
planner says "FINISH" or the step limit is reached.
"""

# Helper functions that manage the shared agent state dictionary.
from Day16.agent.state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    can_continue,
    finish
)


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client
):
    # Build the initial state from the user's request.
    state = create_state(user_request)

    # This is the heart of our agent: keep looping while we still have
    # steps left and the planner hasn't said we're finished.
    while can_continue(state):

        # The planner decides what to do next (an LLM call under the hood).
        action = planner(state, tools)

        print("Planner Selected:", action)

        if action == "FINISH":
            # The planner thinks the request is satisfied; build the final
            # natural-language answer and stop looping.
            answer = format_answer(state)

            finish(state, answer)

            break

        # We execute that action (calls the matching tool on the MCP server).
        observation = await execute_action(
            action,
            state,
            client
        )

        # We add that action to state so the planner won't repeat it.
        add_action(
            state,
            action
        )

        # We remember what happened (the tool's result) for future planning.
        record_observation(
            state,
            action,
            observation
        )

        # We move to the next iteration (increments the step counter).
        next_step(state)

    return state
