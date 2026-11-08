"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This script is a small manual smoke-test for an agent state helper module
(from the earlier Day09 "AgentState" lesson), used to sanity-check that
creating a state, recording actions/observations, advancing the step
counter, and marking the state as finished all work as expected - the same
kind of state transitions that, in this lesson, are driven automatically
by the LangGraph nodes and conditional edges in graph.py.
"""

# NOTE: This imports helper functions (create_state, add_action,
# record_observation, next_step, finish) from the Day09 lesson's state
# module rather than this lesson's own `agent/state.py` (which only
# defines the `AgentState` TypedDict, with no helper functions). This is
# pre-existing behavior from the original lesson material and is left
# unchanged here.
from Day09.agent.state import *

# Create a brand-new state dict for a fresh user request.
state = create_state(
    "Generate a password and tell me the current time."
)

print("Initial State")
print(state)

# Record that the "generate_password" action was chosen/performed.
add_action(
    state,
    "generate_password"
)

# Store the result of that action as an observation tied to its name.
record_observation(
    state,
    "generate_password",
    "Password : X#8Lm@4P"
)

# Advance the step counter, simulating one full plan -> act -> observe loop.
next_step(state)

print("\nState After One Iteration")
print(state)

# Mark the state as finished and attach the final answer text.
finish(
    state,
    "Password : X#8Lm@4P\nCurrent Time : 10:35 AM"
)

print("\nFinal State")
print(state)
