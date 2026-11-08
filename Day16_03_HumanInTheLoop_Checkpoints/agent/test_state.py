"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This is a small standalone smoke-test script for an older, simpler
dictionary-based agent state helper (from the Day09 module), used to sanity
check that creating a state, recording an action/observation, advancing a
step, and finishing produces the expected state transitions. It predates
the LangGraph-based `AgentState` used elsewhere in this folder.
"""

# NOTE: this imports a state helper module from a different day's folder
# (Day09); it is kept as-is since fixing that reference is out of scope here.
from Day09.agent.state import *

# Create a fresh state dict seeded with the user's request.
state = create_state(
    "Generate a password and tell me the current time."
)

print("Initial State")
print(state)

# Simulate the agent choosing and recording a "generate_password" action.
add_action(
    state,
    "generate_password"
)

# Record what that action "observed" (its result).
record_observation(
    state,
    "generate_password",
    "Password : X#8Lm@4P"
)

# Advance the step counter, as the graph would after a tool call.
next_step(state)

print("\nState After One Iteration")
print(state)

# Mark the state as finished with a final combined answer.
finish(
    state,
    "Password : X#8Lm@4P\nCurrent Time : 10:35 AM"
)

print("\nFinal State")
print(state)
