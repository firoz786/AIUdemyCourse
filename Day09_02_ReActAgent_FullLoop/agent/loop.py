"""
Day09_02_ReActAgent_FullLoop - agent/loop.py

This is the heart of the course: the full ReAct (Reason -> Act -> Observe)
loop that ties the planner, executor, and state together. On each
iteration the planner decides the next action (or signals FINISH), the
executor runs that action against the MCP server, the result is recorded
as an observation in the state, and the loop advances to the next step --
repeating until the agent finishes or hits its max step limit.
"""

from state import (
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
    # Start with a brand-new state for this user request.
    state = create_state(user_request)

    # This is the heart of our agent: keep looping while there is still
    # budget left (not finished, and under the max step count).
    while can_continue(state):

        # The planner decides what to do next, based on the current state.
        action = planner(state, tools)

        print("Planner Selected:", action)

        if action == "FINISH":
            # The planner signaled the request is fully satisfied: build
            # the final natural-language answer and stop looping.
            answer = format_answer(state)

            finish(state, answer)

            break

        # We execute that action against the MCP server.
        observation = await execute_action(
            action,
            client
        )

        # We add that action in state so we don't repeat completed work.
        add_action(
            state,
            action
        )

        # We remember what happened (the observation) for this step.
        record_observation(
            state,
            action,
            observation
        )

        # We move to the next iteration.
        next_step(state)

    return state

