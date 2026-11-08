"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

Defines the shared `AgentState` shape used by every node in the LangGraph
graph (see graph.py). Using a single TypedDict keeps the state's fields
consistent and documented in one place as it flows through the planner,
approval, tool, and answer nodes.
"""

from typing import TypedDict


class AgentState(TypedDict):
    """All the fields that are threaded through the LangGraph agent graph."""

    # The original natural-language request from the user.
    user_request: str

    # How many tool-calling steps have been executed so far.
    current_step: int

    # Safety limit on how many steps the agent loop may take.
    max_steps: int

    # The list of tool names that have been executed, in order.
    actions: list

    # The list of {step, action, observation} records from each tool call.
    observations: list

    # The tool name (or "FINISH") chosen by the planner for this step.
    action: str

    # The human's approval decision for the current action ("yes"/"no").
    approval: str

    # Whether the agent loop has completed.
    finished: bool

    # The final natural-language answer shown to the user.
    final_answer: str

