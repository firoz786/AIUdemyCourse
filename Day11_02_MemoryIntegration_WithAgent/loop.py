"""
Day 11.2 - Memory Integration With Agent.

This module contains the core autonomous "agent loop": the plan -> act ->
observe cycle. New in this stage of the course is memory integration -
before planning, the agent searches past conversations for semantically
relevant memories and feeds them into both the planner and the final
answer. When the agent finishes, it also saves the new exchange as a
memory so future requests can benefit from it.
"""

from state import (
    create_state,
    add_task,
    add_action,
    record_observation,
    add_result,
    complete_task,
    all_tasks_completed,
    next_step,
    can_continue,
    finish
)
from memory import save_memory


from task_planner import (
    decompose_task
)
from state import add_memory
from memory import search_semantic_memories


def parse_decision(decision):
    """Pull the TASK and TOOL values out of the planner's raw text reply."""

    task = None
    tool = None

    # Handle the normal two-line format
    for line in decision.splitlines():

        line = line.strip()

        if line.startswith("TASK:"):

            task = line[5:].strip()

        elif line.startswith("TOOL:"):

            tool = line[5:].strip()

    # Handle the case where the LLM puts
    # TASK and TOOL on the same line.
    if task and "TOOL:" in task:

        parts = task.split(
            "TOOL:",
            1
        )

        task = parts[0].strip()

        if not tool:

            tool = parts[1].strip()

    return task, tool


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client
):
    """Run the full agent cycle for one user request: recall memories,
    plan tasks, then repeatedly pick a tool, execute it, and record the
    outcome until the plan is complete or the step limit is reached."""

    # Create a fresh, empty state dict for this single request.
    state = create_state(
        user_request
    )

    # Look up past memories that are semantically similar to this request.
    memories = search_semantic_memories(
        user_request,
        top_k=3
    )

    # Stash each relevant memory into the state so the planner/answer can use it.
    for memory in memories:
        add_memory(
            state,
            memory
        )

    # --------------------------------
    # Step 1: Decompose the goal
    # --------------------------------

    # Ask the LLM to break the request into an ordered list of small tasks.
    planned_tasks = decompose_task(
        user_request
    )

    for task in planned_tasks:

        add_task(
            state,
            task
        )

    print("\nTask Plan")
    print("---------")

    for item in state["tasks"]:

        print(
            "-",
            item["task"]
        )

    # --------------------------------
    # Step 2: Autonomous loop
    # --------------------------------

    # Keep looping while the agent hasn't finished and hasn't hit max_steps.
    while can_continue(state):

        # --------------------------------
        # Check whether all tasks are done
        # --------------------------------

        if all_tasks_completed(state):

            print(
                "\n--- Step "
                f"{state['current_step'] + 1} ---"
            )

            print(
                "Planner Decision:"
            )

            print("TASK: FINISH")

            # All tasks are complete, so generate the final answer now.
            answer = format_answer(
                state
            )

            finish(
                state,
                answer
            )

            break

        print(
            f"\n--- Step "
            f"{state['current_step'] + 1} ---"
        )

        # --------------------------------
        # Ask planner for next task
        # --------------------------------

        # Ask the LLM planner which pending task/tool to run next.
        decision = planner(
            state,
            tools
        )

        print(
            "Planner Decision:"
        )

        print(decision)

        # --------------------------------
        # Check FINISH
        # --------------------------------

        if decision.strip().upper() == "FINISH":

            # The planner decided no more tool calls are needed.
            answer = format_answer(
                state
            )

            finish(
                state,
                answer
            )

            # Save this request/answer pair as a long-term memory for later use.
            save_memory(
                user_request,
                answer
            )

            break

        # --------------------------------
        # Extract task and tool
        # --------------------------------

        # Parse the planner's reply into the task text and the tool to call.
        task, tool = parse_decision(
            decision
        )

        if not task or not tool:

            # The planner's reply didn't match the expected format;
            # record the issue and try again on the next step.
            add_result(
                state,
                "Invalid planner decision."
            )

            next_step(state)

            continue

        state["current_task"] = task

        # --------------------------------
        # Execute tool
        # --------------------------------

        # Run the chosen tool through MCP and capture its output.
        observation = await execute_action(
            tool,
            state,
            client
        )

        print(
            "Observation:",
            observation
        )

        # --------------------------------
        # Update state
        # --------------------------------

        add_action(
            state,
            tool
        )

        record_observation(
            state,
            tool,
            observation
        )

        add_result(
            state,
            observation
        )

        # --------------------------------
        # Mark task complete
        # --------------------------------

        if not observation.lower().startswith(
            "error"
        ):

            # Tool succeeded, so mark the matching task as completed.
            complete_task(
                state,
                task
            )

            print(
                "completed"
            )

        else:

            # Tool failed; leave the task pending so the planner retries it.
            add_result(
                state,
                "The previous action failed. "
                "The planner must reconsider."
            )

        next_step(state)

    return state
