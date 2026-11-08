"""
Day16_01 - LangGraph Basic Graph: shared state schema.

This file defines AgentState, the TypedDict that describes the shape of
the "state" dictionary passed between LangGraph nodes (see graph.py).
LangGraph uses this schema to know which keys exist and how they should
be typed; every node reads from and returns updates to this same shape.
"""

from typing import TypedDict


class AgentState(TypedDict):
    # The original request/question from the user.
    user_request: str
    # How many plan/act steps have been taken so far.
    current_step: int
    # Safety limit on how many steps the agent is allowed to take.
    max_steps: int
    # List of actions (tool names) that have already been performed.
    actions: list
    # List of observations (tool results) collected so far.
    observations: list
    # True once the planner has decided the task is complete.
    finished: bool
    # The final natural-language answer to show the user.
    final_answer: str

