"""
Day13_03 - Registry Integration: The Complete Loop
====================================================
This module implements the core "agent loop": plan -> act -> observe,
repeated until the planner says FINISH or the step limit is reached.
It's deliberately generic (it takes `planner`, `execute_action`, and
`format_answer` as arguments) so the same loop can drive different
planning/execution strategies without being rewritten - including the
mixed local/remote MCP server setup used in this folder.
"""
from state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    can_continue,
    finish
)


async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, tool_registry):
    """Drive the plan -> act -> observe loop until the task is finished."""
    state = create_state(user_request)

    while can_continue(state):
        # Ask the planner to decide the single next action to take.
        action = planner(state, tools)
        print("Planner Selected:", action)

        if action["tool"] == "FINISH":
            # The planner thinks the request is fully handled; produce
            # the final natural-language answer and stop looping.
            answer = format_answer(state)
            finish(state, answer)
            break

        # Run the chosen tool and record what happened so the planner
        # can see it on the next iteration.
        observation = await execute_action(action, state, tool_registry)
        add_action(state, action)
        record_observation(state, action, observation)
        next_step(state)

    return state

