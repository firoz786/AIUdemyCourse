"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This small module is the standalone definition of the agent's shared
state shape, mirroring the `AgentState` also defined inline in graph.py.
It documents the "memory" that flows through every LangGraph node and
that the conditional edge functions (`route_after_planner`,
`route_after_tool`) read to decide which node should run next.
"""

from typing import TypedDict


class AgentState(TypedDict):
    user_request: str      # The original question/task from the user.
    current_step: int      # How many planner/tool iterations have run so far.
    max_steps: int          # Safety limit to stop infinite planning loops.
    actions: list            # History of every action (tool name) chosen.
    observations: list      # History of results returned by each tool call.
    action: str              # The action the planner just chose this turn.
    finished: bool            # True once the agent is done and ready to answer.
    final_answer: str        # The natural-language answer shown to the user.
