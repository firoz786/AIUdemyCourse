"""
Day 15 - Production Engineering & Resilience: Multi-Agent Manager/Orchestrator.

This file is the heart of the resilient multi-agent system: `run_manager`
validates the incoming task, then repeatedly asks an LLM-powered
`choose_worker` function which worker (research, coding, review, or finish)
should act next, routes to that worker, and tracks revision history so the
coding/review loop can't run forever (bounded by MAX_REVISIONS). It ties
together config, logging, validation, and resilient LLM calls (via
call_llm's built-in retry/backoff) into one cohesive, observable workflow.
"""

from llm import call_llm
from validation import (
    validate_task
)

from logger import logger

from workers.research_agent import research
from workers.coding_agent import write_code
from workers.reviewer_agent import review
from agent.state import create_state

from config import (
    MAX_REVISIONS
)


def choose_worker(state):
    # Build a prompt that gives the LLM full context of the current workflow
    # state (what's been done so far) so it can decide the next step.
    prompt = f"""
You are the Manager Agent.

Your job is to decide which worker
should act NEXT.

Original Task:
{state["task"]}

Research:
{state["research"]}

Code:
{state["code"]}

Review:
{state["review"]}

History:
{state["history"]}

Revision Count:
{state["revision_count"]}

Maximum Revisions:
{MAX_REVISIONS}

Available workers:

research
coding
review
finish

Decision rules:

- If Research is empty, choose research.

- If Research exists and Code is empty, choose coding.

- If a Review exists with status
  "needs_revision" and the Revision count is below the maximum, choose coding.

- If Code exists and there is no Review, choose review.

- If the previous review requested
  revision and new code has been generated,  choose review again.

- If the latest Review status is
  "approved", choose finish.

- If the maximum revision count has
  been reached, choose finish.

Return ONLY one word:

research
coding
review
finish
"""
    # Ask the LLM (with built-in retry/backoff) which worker to run next.
    response = call_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Normalize the reply (strip whitespace, lowercase) so comparisons like
    # `worker == "research"` below are reliable.
    return response.strip().lower()


def run_manager(task):
    # Validate the task first (non-empty, not too long) before doing any
    # expensive LLM work - fail fast on bad input.
    task = validate_task(task)
    state = create_state(
        task
    )
    # Record the start of the workflow for observability/debugging.
    logger.info(
    f"Starting manager for task: {task}"
    )

    # Main orchestration loop: keep asking "what's next?" until a worker
    # tells us to finish (or we hit the revision cap).
    while True:

        worker = choose_worker(
            state
        )
        # Log and print the manager's decision so progress is visible.
        logger.info(
    f"Manager selected: {worker}"
        )

        print(
            f"\nManager selected: {worker}"
        )

        if worker == "research":
            # Run the research worker and store its findings in state.
            state["research"] = research(
                state["task"]
            )

            state["history"].append(
                "research"
            )

        elif worker == "coding":
            # Safety valve: if we've already hit the max revisions, stop
            # instead of looping forever on a stubborn review.
            if (
            state["review"]
            and state["revision_count"]
            >= MAX_REVISIONS
            ):

                print(
                "Maximum revisions reached."
                )
                # Warn in the logs since this is an abnormal/bounded exit.
                logger.warning(
        f"Maximum steps reached: {MAX_REVISIONS}"
                )

                break

            # Pull feedback from the previous review (if any) so the coding
            # agent knows what to fix.
            feedback = ""

            if state["review"]:

                feedback = state[
                "review"
                ].get(
                "feedback",
                ""
                )

            # Track how many revision cycles have happened so far.
            state["revision_count"] += 1

            # Generate (or regenerate) the code using task, research and
            # any reviewer feedback.
            state["code"] = write_code(
            state["task"],
            state["research"],
            feedback
            )

            # Clear the previous review since the code has changed and
            # needs to be reviewed again.
            state["review"] = ""

            state["history"].append(
            "coding"
            )

        elif worker == "review":
            # Ask the reviewer agent to check the latest code.
            state["review"] = review(
                state["task"],
                state["code"]
            )

            state["history"].append(
                "review"
            )

        elif worker == "finish":
            # The manager decided the workflow is complete - stop looping.
            logger.info(
            "Manager finished the workflow."
            )

            break

        else:
            # Defensive check: the LLM returned something we don't recognize.
            raise ValueError(
                f"Unknown worker: {worker}"
            )

    return state
